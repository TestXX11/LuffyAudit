#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from django.shortcuts import render, \
    redirect, \
    HttpResponse
from django.contrib.auth import authenticate, login, logout     # django 登录组件
from django.contrib.auth.decorators import login_required
from audit import models
from audit import task_handler

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
        # django 自带登录验证
        user = authenticate(username=username, password=password)
        if user:  #  如果用户存在跳到主页面   django 自动设置 session
            login(request, user)  # django自带登录
            return redirect(request.GET.get('next') or '/')         #
        else:
            error = 'Wrong username or password!'   # 帐号验证失败
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
    gid = request.GET.get('gid')    # 获取组 id
    if gid:
        if gid == '0':  # 未分组
            host_list = request.user.account.host_user_binds.all() # 读取组主机列表
        else:
            # host_list = request.user.account.host_groups.filter
            group_obj = request.user.account.host_groups.get(id=gid)    # 获取组对象
            host_list = group_obj.host_user_binds.all()             # 获取组列表
        # 获取每个主机的信息,用 list 迭代,然后序列化
        data = json.dumps(list(host_list.values('id', 'host__hostname', 'host__ip_addr',
                                                'host__port', 'host_user__username', 'host__idc__name')))
        # 返回给前端
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
    time_obj = timezone.now() - datetime.timedelta(seconds=300)  # 5min ago time out
    # 获取当前这个用户生成的没有过期的 token
    exist_token_objs = models.Token.objects.filter(account=request.user.account.id,
                                                   host_user_bind=bind_host_id,
                                                   date__gt=time_obj)
    # token_data = {}
    # 如果这个 token 存在
    if exist_token_objs:  # has token already
        token_data = {'token': exist_token_objs[0].val}     # 通过索引取值
        # token_data['token'] = exist_token_objs[0].val
    else:       # 如果这个 token 不存在就为这个主机生成当前用户专属的 token
        token_val = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
        print(token_val)
        # 把 token 放到数据库
        token_obj = models.Token.objects.create(
            host_user_bind_id=bind_host_id,
            account=request.user.account,
            val=token_val
        )
        token_data = {'token': token_val}
        # token_data['token'] = token_val

    return HttpResponse(json.dumps(token_data))

@login_required
def multi_cmd(request):
    '''批量命令 html'''
    return render(request,'multi_cmd.html')


@login_required
def multitask(request):
    '''调用相关函数,脚本来批量执行任务'''
    task_obj = task_handler.Task(request)   # 实例化
    print('request post :',request.POST)
    print('task_obj',task_obj)
    if task_obj.is_valid():     # 验证是否有命令 and 主机
        result = task_obj.run()     # 执行任务
        return HttpResponse(json.dumps({'task_id':result}))     # 返回执行结果
    return HttpResponse(json.dumps(task_obj.errors))    # 返回错误信息



def multitask_result(request):
    '''
    获取任务的执行状态
    :param request:
    :return:
    '''
    task_id = request.GET.get('task_id')    # 获取任务 id

    task_obj = models.Task.objects.get(id=task_id)

    result = list(task_obj.tasklog_set.values('id','status',
                                              'host_user_bind__host__hostname',
                                              'host_user_bind__host__ip_addr',
                                              'result'))
    return HttpResponse(json.dumps(result))

