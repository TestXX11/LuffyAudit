import time
import sys
import os
import paramiko
import multiprocessing


def cmd_run(tasklog_id, cmd):
    try:
        import django
        django.setup()
        from audit import models
        tasklog_obj = models.TaskLog.objects.get(id=tasklog_id)
        print('run cmd:', tasklog_obj, cmd)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(tasklog_obj.host.host.ip_addr,
                    tasklog_obj.host.host.port,
                    tasklog_obj.host.host_user.username,
                    tasklog_obj.host.host_user.password,
                    timeout=15)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read() + stderr.read()
        print('------------%s----------\n' % tasklog_obj.host, result)
        ssh.close()

        tasklog_obj.result = result or 'cmd has no result output'
        tasklog_obj.status = 0
        tasklog_obj.save()
    except Exception as e:
        print('error:', e)


def file_transfer(host):
    pass


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jackupdownAudit.settings")
    import django
    django.setup()
    from audit import models

    task_id = sys.argv[1]
    #1. 根据Taskid拿到任务对象，
    #2. 拿到任务关联的所有主机
    #3.  根据任务类型调用多进程 执行不同的方法
    #4 . 每个子任务执行完毕后，自己八结果写入数据库
    task_obj = models.Task.objects.get(id=task_id)
    pool = multiprocessing.Pool(processes=10)
    if task_obj.type == 0:  # cmd
        func = cmd_run
    else:
        func = file_transfer
    for host in task_obj.tasklog_set.all():
        pool.apply_async(func, args=(host.id, task_obj.id, task_obj.content))
    pool.close()
    print('------------------\n', task_obj)
    pool.join()

