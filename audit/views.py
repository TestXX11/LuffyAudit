from django.shortcuts import render,HttpResponse,redirect
from audit import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
import json

@login_required
def index(request):



    return render(request,'index.html')


def acc_login(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(username=username,password=pwd)
        if user:
            login(request,user)
            #next为由哪个页面跳转来的，登录后跳转至哪个页面
            return redirect(request.GET.get('next') or '/')
        else:
            error = '用户名或密码错误！'

    return render(request,'login.html',{'error':error})


@login_required
def acc_logout(request):
    logout(request)
    return redirect('/login.html')


@login_required
def host_list(request):

    return render(request,'hostlist.html')


@login_required
def get_host_list(request):
    if request.method == 'GET':
        gid = request.GET.get('gid')
        if gid:
            if gid == '-1':
                host_list = request.user.account.host_user_binds.all()
            else:
                group_obj = request.user.account.host_groups.get(id=gid)
                host_list = group_obj.host_user_binds.all()

            data = json.dumps(list(host_list.values('id', 'host__hostname', 'host__ip_addr', 'host__port',
                                                    'host__idc__name','host_user__username')))
            return HttpResponse(data)
