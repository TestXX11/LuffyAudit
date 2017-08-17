import time
import sys
import os
import paramiko
import json
import multiprocessing


def cmd_run(tasklog_id, task_id, cmd):
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
        print('cmd run error:', e)
        tasklog_obj.status = 1
        tasklog_obj.result = str(e)
        tasklog_obj.save()


def file_transfer(tasklog_id, task_id, task_content):
    import django
    django.setup()
    from django.conf import settings
    from audit import models
    tasklog_obj = models.TaskLog.objects.get(id=tasklog_id)
    print('run file_transfer:', tasklog_obj, task_id, task_content)
    try:
        task_data = json.loads(tasklog_obj.task.content)
        t = paramiko.Transport((tasklog_obj.host.host.ip_addr, tasklog_obj.host.host.port))
        t.connect(username=tasklog_obj.host.host_user.username, password=tasklog_obj.host.host_user.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if task_data.get('file_transfer_type') == 'send':
            local_path = os.path.join(settings.FILE_UPLOADS, str(tasklog_obj.task.account.id), task_data.get('random_str'))
            print('local_path...send', local_path)
            for file_name in os.listdir(local_path):
                print('for............file name', file_name, task_data.get('remote_path'))
                sftp.put(os.path.join(local_path, file_name), os.path.join(task_data.get('remote_path'), file_name))
            tasklog_obj.result = "send all files done...."
        else:
            # 从远程服务器下载文件
            download_dir = os.path.join(settings.FILE_DOWNLOADS, str(task_id))
            print(download_dir, '-------------------------------------', os.path.isdir(download_dir))
            if not os.path.isdir(download_dir):
                os.makedirs(download_dir, exist_ok=True)
            print('....remote_filename.....',task_data.get('remote_path'))
            remote_filename = os.path.basename(task_data.get('remote_path'))
            print('remote_filename........', remote_filename)
            local_path = os.path.join(download_dir, tasklog_obj.host.host.ip_addr+'.'+remote_filename)
            print('file_transfer...local_path', local_path)
            sftp.get(task_data.get('remote_path'), local_path)
            tasklog_obj.result = "get remote file [%s] to local done..." % task_data.get('remote_path')
        t.close()
        tasklog_obj.status = 0
        tasklog_obj.save()
    except Exception as e:
        print('file transfer error:', e)
        tasklog_obj.status = 1
        tasklog_obj.result = str(e)
        tasklog_obj.save()



if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    #print(BASE_DIR, 'multitask base dir......................................')
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jackupdownAudit.settings")
    import django
    django.setup()
    from audit import models

    task_id = sys.argv[1]
    #print('task id .........', task_id, type(task_id),int(task_id), '\n')

    #test = models.Task.objects.get(id=20)
    #print(test.id, test.type, '....test..........\n')
    #task_id = sys.argv[1]
    #print('....task id....', task_id, type(task_id))
    #1. 根据Taskid拿到任务对象，
    #2. 拿到任务关联的所有主机
    #3.  根据任务类型调用多进程 执行不同的方法
    #4 . 每个子任务执行完毕后，自己八结果写入数据库
    task_obj = models.Task.objects.get(id=int(task_id))
    pool = multiprocessing.Pool(processes=10)
    if task_obj.type == 0:  # cmd
        print('run cmd......cmd .....\n')
        func = cmd_run
    else:
        func = file_transfer
    for host in task_obj.tasklog_set.all():
        print(host.id, task_obj.id, task_obj.content)
        pool.apply_async(func, args=(host.id, task_obj.id, task_obj.content))
        #pool.apply_async(func, args=(host.id, task_obj.id, task_obj.content))
    pool.close()
    print('-----pool close-------------\n', task_obj)
    pool.join()

