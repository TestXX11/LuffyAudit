from django.shortcuts import render,\
                            redirect,\
                            HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

import json

# Create your views here.
def index(request):
    return render(request,'index.html')

def acc_login(request):
    error = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user :           # 如果用户存在跳到主页面   django 自动设置 session
            login(request,user)
            return redirect(request.GET.get('next') or '/')
        else:
            error = 'Wrong username or password!'
    return render(request,'login.html',{'error',error})

def acc_logout(request):
    logout(request)
    return redirect('/login/')

def host_list(request):

    return render(request,'hostlist.html')

@login_required
def get_host_list(request):
    gid = request.GET.get('gid')
    if gid:
        if gid == '0':  # 未分组
            host_list = request.user.account.host_user_binds.all()
        else:
            # host_list = request.user.account.host_groups.filter
            group_obj = request.user.account.host_groups.get(id=gid)
            host_list = group_obj.host_user_binds.all()
        data = json.dumps(list(host_list.values('id','host__hostname','host__ip_addr',
                                                'host__port','host_user__username')))
        return HttpResponse(data)