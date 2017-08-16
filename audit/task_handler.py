import json
import subprocess
from django.conf import settings
from django.db.transaction import atomic
from audit import models


class Task(object):
    """处理批量任务，包括执行命令和传输文件"""
    def __init__(self, request):
        self.request = request
        self.errors = []
        self.task_data = None

    def is_valid(self):
        """验证任务和主机列表是否合法"""
        task_data = self.request.POST.get('task_data')
        if task_data:
            self.task_data = json.loads(task_data)
            if self.task_data.get('type') == 'cmd':
                if self.task_data.get('cmd') and self.task_data.get('host_list'):
                    return True
                self.errors.append({'invalid argument': 'cmd or host list is empty'})
            elif self.task_data.get('type') == 'file_transfer':
                self.errors.append({'invalid argument': 'developing...'})
            else:
                self.errors.append({'invalid argument': 'task type is invalid'})
        self.errors.append({'invalid data': 'task data is not exist'})

    def run(self):
        """执行任务并返回任务id"""
        task_func = getattr(self, self.task_data.get('type'))
        task_id = task_func()
        return task_id

    @atomic
    def cmd(self):
        """批量命令"""
        task_obj = models.Task.objects.create(
            type=0,
            account=self.request.user.account,
            content=self.task_data.get('cmd'),
        )
        tasklog_objs = []
        host_ids = set(self.task_data.get('host_list'))
        for host_id in host_ids:
            tasklog_objs.append(
                models.TaskLog(
                    task_id=task_obj.id,
                    host_id=host_id,
                    status=3,
                )
            )
        models.TaskLog.objects.bulk_create(tasklog_objs, 100)

        cmd_str = "python %s %s" % (settings.MULTI_TASK_SCRIPT, task_obj.id)
        multitask_obj = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return task_obj.id

    def run_cmd(self):
        pass

    def file_transfer(self):
        pass