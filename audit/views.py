from django.shortcuts import render,HttpResponse,redirect
from audit import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
import json,datetime,string,random


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


@login_required
def start_cmd(request):

    return render(request,'start_cmd.html')


@login_required
def get_token(request):
    """生成token并返回"""

    if request.method == 'POST':
        """查找未过期的属于这台主机的口令，如同一台主机未过期则不再生成，超时生成新口令"""

        time_obj = datetime.datetime.now() - datetime.timedelta(seconds=300)
        gid = request.POST.get('gid')
        exist_token = models.Token.objects.filter(host_user_bind_id=gid,
                                                  account=request.user.account,
                                                  date__gt=time_obj).first()

        print(time_obj)

        if exist_token:
            token_obj = {'token':exist_token.val}

        else:
            token_val = ''.join(random.sample(string.ascii_lowercase+string.digits,8))
            models.Token.objects.create(host_user_bind_id=gid,account=request.user.account,val = token_val)
            token_obj = {'token':token_val}
        print(token_obj)

        return HttpResponse(json.dumps(token_obj))