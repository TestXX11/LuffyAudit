from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import os
from audit import models
import random
import string
import datetime
from audit import task_handler
from django.conf import settings
import zipfile
from wsgiref.util import FileWrapper    #from django.core.servers.basehttp import FileWrapper以前的位置


# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')


def acc_login(request):
    error = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next') or '/')
        else:
            error = "Wrong username or password!"
    return render(request, 'login.html', {'error': error})


@login_required
def acc_logout(request):
    logout(request)
    return redirect('/login/')


@login_required
def host_list(request):
    return render(request, 'hostlist.html')


@login_required
def get_host_list(request):
    gid = request.GET.get('gid')
    if gid:
        if gid == '-1':  # 未分组
            host_list = request.user.account.host_user_binds.all()
        else:
            group_obj = request.user.account.host_groups.get(id=gid)
            host_list = group_obj.host_user_binds.all()
        data = json.dumps(
            list(host_list.values('id', 'host__hostname', 'host__ip_addr', 'host__idc__name', 'host__port',
                                  'host_user__username')))
        return HttpResponse(data)


@login_required
def get_token(request):
    """生成token并返回"""
    bind_host_id = request.POST.get('bind_host_id')
    time_obj = datetime.datetime.now() - datetime.timedelta(seconds=300)
    exist_token_objs = models.Token.objects.filter(account_id=request.user.account.id,
                                                   host_user_bind_id=bind_host_id,
                                                   date__gt=time_obj)
    if exist_token_objs:
        token_data = {'token': exist_token_objs[0].val}
    else:
        token_val = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
        token_obj = models.Token.objects.create(
            host_user_bind_id=bind_host_id, account=request.user.account, val=token_val
        )
        token_data = {'token': token_val}
    return HttpResponse(json.dumps(token_data))


@login_required
def multi_cmd(request):
    return render(request, 'multi_cmd.html')


@login_required
def multitask(request):
    task_obj = task_handler.Task(request)
    print('multitask', task_obj)
    if task_obj.is_valid():
        print('before multi task.....')
        obj = task_obj.run()
        print('multi task result', obj, obj.id)
        return HttpResponse(json.dumps({'task_id': obj.id, 'timeout': obj.timeout}))
    return HttpResponse(json.dumps(task_obj.errors))


@login_required
def multitask_result(request):
    task_id = request.GET.get('task_id')
    task_obj = models.Task.objects.get(id=int(task_id))
    results = list(task_obj.tasklog_set.values(
        'id', 'status', 'host__host__hostname', 'host__host__ip_addr', 'result'
    ))
    return HttpResponse(json.dumps(results))


@login_required
def multi_file_transfer(request):
    random_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
    return render(request, 'multi_file_transfer.html', locals())


@login_required
@csrf_exempt
def task_file_upload(request):
    random_str = request.GET.get('random_str')
    upload_to = os.path.join(settings.FILE_UPLOADS, str(request.user.account.id), random_str)
    if not os.path.isdir(upload_to):
        os.makedirs(upload_to)
    file_obj = request.FILES.get('file')
    f = open(os.path.join(upload_to, file_obj.name), 'wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()
    print(file_obj,'task_file_upload')
    return HttpResponse(json.dumps({'status': 0}))


def send_zipfile(request, task_id, file_path):
    """
    Create a ZIP file on disk and transmit it in chunks of 8KB,
    without loading the whole file into memory. A similar approach can
    be used for large dynamic PDF files.
    """
    zip_file_name = 'task_id_%s_files' % task_id
    archive = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
    file_list = os.listdir(file_path)
    for filename in file_list:
        archive.write(os.path.join(file_path, filename), arcname=filename)
    archive.close()

    wrapper = FileWrapper(open(zip_file_name, 'rb'))
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % zip_file_name
    response['Content-Length'] = os.path.getsize(zip_file_name)
    return response


@login_required
def task_file_download(request):
    task_id = request.GET.get('task_id')
    print(task_id)
    task_file_path = os.path.join(settings.FILE_DOWNLOADS, task_id)
    return send_zipfile(request, task_id, task_file_path)

















