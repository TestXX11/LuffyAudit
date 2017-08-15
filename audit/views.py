from django.shortcuts import render, \
    redirect, \
    HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from audit import models

import json, \
    random, \
    string, \
    datetime


# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')


def acc_login(request):
    '''
    帐号登录
    :param request:
    :return:
    '''
    error = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:  # 如果用户存在跳到主页面   django 自动设置 session
            login(request, user)  # django自带登录
            return redirect(request.GET.get('next') or '/')
        else:
            error = 'Wrong username or password!'
    return render(request, 'login.html', {'error': error})


@login_required
def acc_logout(request):
    '''
    注销登录
    :param request:
    :return:
    '''
    logout(request)  # django 自带注销登录
    return redirect('/login/')


@login_required
def host_list(request):
    '''
    主机列表页面
    :param request:
    :return:
    '''
    return render(request, 'hostlist.html')


@login_required  # 下面这个方法要求用户登录验证
def get_host_list(request):
    '''
    获取主机组下的所有主机
    :param request:
    :return:
    '''
    gid = request.GET.get('gid')
    if gid:
        if gid == '0':  # 未分组
            host_list = request.user.account.host_user_binds.all()
        else:
            # host_list = request.user.account.host_groups.filter
            group_obj = request.user.account.host_groups.get(id=gid)
            host_list = group_obj.host_user_binds.all()
        data = json.dumps(list(host_list.values('id', 'host__hostname', 'host__ip_addr',
                                                'host__port', 'host_user__username', 'host__idc__name')))
        return HttpResponse(data)


@login_required
def get_token(request):
    '''
    生成 token
    :param request:
    :return:
    '''
    print(request.POST)
    bind_host_id = request.POST.get('bind_host_id')  # 获取相关联的主机 id
    # time_obj = datetime.datetime.now() - datetime.timedelta(seconds=300)    # 5min ago

    # 由于更改了时区,会出现报错的问题
    from django.utils import timezone
    time_obj = timezone.now() - datetime.timedelta(seconds=300)  # 5min ago

    exist_token_objs = models.Token.objects.filter(account=request.user.account.id,
                                                   host_user_bind=bind_host_id,
                                                   date__gt=time_obj)
    # token_data = {}
    if exist_token_objs:  # has token already
        token_data = {'token': exist_token_objs[0].val}
        # token_data['token'] = exist_token_objs[0].val
    else:
        token_val = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
        print(token_val)
        token_obj = models.Token.objects.create(
            host_user_bind_id=bind_host_id,
            account=request.user.account,
            val=token_val
        )
        token_data = {'token': token_val}
        # token_data['token'] = token_val

    return HttpResponse(json.dumps(token_data))
