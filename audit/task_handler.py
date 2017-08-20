#!/usr/bin/env python3  
#-*- coding: utf-8 -*-
#@time : 2017/08/16

import json,\
    subprocess,\
    sys

from audit import models
from threading import Thread
from django.conf import settings
from django.db.transaction import atomic        # 原子操作

class Task(object):
    '''
    处理批量任务,包括命令和文件传输
    '''
    def __init__(self,request):
        self.request = request
        self.errors = []
        self.task_data = None

    def is_valid(self):
        '''
        验证命令,主机列表是否合法,
        :return:
        '''
        task_data = self.request.POST.get('task_data')
        if task_data:       # 验证数据
            self.task_data = json.loads(task_data)  # 序列化
            # cmd
            print('cmd: ', self.task_data)
            if self.task_data.get('task_type') == 'cmd':    # shell 命令
                if self.task_data.get('cmd') and self.task_data.get('selected_host_ids'):
                    # 有shell命令并且有目标主机
                    return True
                #
                self.errors.append({'invalid_argument':'cmd or host_list or empty'})
            # file
            elif self.task_data.get('task_type') == 'file_transfer':
                self.errors.append({"invalid_argument":'cmd or host_list or empty'})
            # 其它
            else:
                self.errors.append({'invalid_argument':'task_type is invalid'})
        # 没有收到字典
        self.errors.append({'invalid_data':'task_data is not exist.'})


    def run(self):
        '''start task , and return task id'''
        task_func = getattr(self,self.task_data.get('task_type'))   # 获取相关的函数
        task_obj = task_func()
        print('task_obj',task_obj)
        return task_obj


    @atomic
    def cmd(self):
        '''批量 cmd 任务'''
        print('run multi task...')
        # 创建任务日志
        task_obj = models.Task.objects.create(
            task_type = 0,
            account = self.request.user.account,
            content = self.task_data.get('cmd'),
        )
        tasklog_objs = []
        # 对主机进行去重
        host_ids = set(self.task_data.get("selected_host_ids"))
        for host_id in host_ids:
            # 创建单条记录信息
            tasklog_objs.append(
                models.TaskLog(task_id =task_obj.id,
                               host_user_bind_id=host_id,
                               status=3))
        # 添加到数据库
        models.TaskLog.objects.bulk_create(tasklog_objs, 100)
        # for host_id in self.task_data.get('selected_host_ids'):
        #     t = Thread(target=self.run_cmd,args=(host_id,self.task_data.get('cmd')))
        #     t.start()
        # print(sys.path)
        # 拼接需要执行任务的 shell 语句  shell 脚本路径 和需要的参数
        cmd_str = "python3 %s %s"%(settings.MULTI_TASK_SCRIPT,task_obj.id)
        # cmd_str = 'ls'
        # 执行命令
        print(sys.path,'cmd_str:',cmd_str)
        multitask_obj = subprocess.Popen(cmd_str,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         shell=True
                                         )
        # multitask_obj = subprocess.Popen(cmd_str,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        # print(multitask_obj.stdout.read())
        return task_obj  # 返回任务 id

    def run_cmd(self):
        pass

    def file_transfer(self):
        ''' 批量文件'''