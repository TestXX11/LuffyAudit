import subprocess, \
    random, \
    string, \
    getpass,\
    datetime

from audit import models
from django.conf import settings
from django.contrib.auth import authenticate
from audit.backend import ssh_interactive


class UserShell(object):
    """用户登录堡垒机后的shell"""

    def __init__(self, sys_argv):
        self.sys_argv = sys_argv  # 接收的参数
        self.user = None  # 初始化登录的用户

    def auth(self):
        '''
        username,password 返回登录结果
        :return:
        '''
        count = 0
        while count < 3:
            username = input("username:").strip()
            password = getpass.getpass("password:").strip()
            # Django 使用自带登录认证
            user = authenticate(username=username, password=password)
            # None 代表认证不成功
            # user object ，认证对象 ,user.name
            if not user:
                count += 1  # 登录计数
                print("Invalid username or password!")
            else:
                self.user = user  # 登录成功  user 是一个对象
                return True  # 必须返回 True
        else:
            print("too many attempts.")  # 错误次数过多

    def token_auth(self):
        count = 0
        while count < 3:
            user_input = input("Input your access token,press Enter if doesn't have:" ).strip()
            if len(user_input) == 0:
                return
            if len(user_input) != 8:
                print('token length is 8')
            else:
                from django.utils import timezone       # 由于更改了时区不能用 datetime.datetime.new()
                time_obj = timezone.now() - datetime.timedelta(seconds=300)
                token_obj = models.Token.objects.filter(val=user_input,date__gt=time_obj).first()
                if token_obj:
                    # token_obj = token_objs.latest()
                    if token_obj.val == user_input:     # token 验证通过
                        self.user = token_obj.account.user      # token  user
                        return token_obj
            count+=1


    def start(self):
        """启动交互程序"""
        token_obj =self.token_auth()
        # token auth
        if token_obj:
            ssh_interactive.ssh_session(token_obj.host_user_bind,self.user)
            exit()
        # shell or terminal / 终端   auth
        if self.auth():
            # print(self.user.account.host_user_binds.all()) #select_related()
            while True:
                # 获取当前用户的所控制的主机组
                host_groups = self.user.account.host_groups.all()
                # 循环主机组,打印出索引,组名,主机数
                for index, group in enumerate(host_groups):
                    print("%s.\t%s[%s]" % (index, group, group.host_user_binds.count()))
                # 未分组的机器,主机数
                print("%s.\t未分组机器[%s]" % (len(host_groups), self.user.account.host_user_binds.count()))
                try:

                    # 让用户选择
                    choice = input("select group>:").strip()
                    if choice.isdigit():  # 用户输入是数字
                        choice = int(choice)  # 强转
                        host_bind_list = None  # 主机列表
                        if choice >= 0 and choice < len(host_groups):
                            selected_group = host_groups[choice]  # 通过索引取用户选择的组
                            host_bind_list = selected_group.host_user_binds.all()
                        elif choice == len(host_groups):  # 选择的未分组机器
                            # selected_group = self.user.account.host_user_binds.all()
                            host_bind_list = self.user.account.host_user_binds.all()
                        if host_bind_list:
                            while True:  # 列出主机索引,主机地址
                                for index, host in enumerate(host_bind_list):
                                    print("%s.\t%s" % (index, host,))
                                choice2 = input("select host>:").strip()
                                if choice2.isdigit():  # 选择了某台主机
                                    choice2 = int(choice2)
                                    if choice2 >= 0 and choice2 < len(host_bind_list):
                                        selected_host = host_bind_list[choice2]  # 获取当前选中的主机
                                        ssh_interactive.ssh_session(selected_host, self.user)

                                        # s = string.ascii_lowercase + string.digits  # 生成所有小写字母 + 数字
                                        # random_tag = ''.join(random.sample(s,10))   # 随机取10个字符
                                        # session_obj = models.SessionLog.objects.create(
                                        #                 account=self.user.account,
                                        #                 host_user_bind=selected_host)
                                        # cmd = "sshpass -p %s /usr/local/openssh/bin/ssh %s@%s -p %s -o" \
                                        #       "StrictHostKeyChecking=no -Z %s"%(
                                        #                             selected_host.host_user.password,
                                        #                             selected_host.host_user.username,
                                        #                             selected_host.host.ip_addr,
                                        #                             selected_host.host.port,
                                        #                             random_tag)
                                        # session_tracker_script = "/bin/sh %s %s %s"%(
                                        #                             settings.SESSION_TRACKER_SCRIPT,
                                        #                             random_tag,
                                        #                             session_obj.id)
                                        # session_tracker_obj = subprocess.Popen(
                                        #                             session_tracker_script,
                                        #                             shell=True,
                                        #                             stdout=subprocess.PIPE,
                                        #                             stderr=subprocess.PIPE)
                                        # ssh_channel = subprocess.run(cmd,shell=True)
                                        # print("selected host", selected_host)
                                        # print(session_tracker_obj.stdout.read(),session_tracker_obj.stderr.read())
                                elif choice2 == 'b':
                                    break

                except KeyboardInterrupt as e:
                    exit()
