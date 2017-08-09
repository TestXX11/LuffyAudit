__author__ = 'Administrator'
from django.contrib.auth import authenticate


class UserShell(object):
    """用户登录堡垒机后的shell"""

    def __init__(self, sys_argv):
        self.sys_argv = sys_argv    # 接收的参数
        self.user = None            # 初始化登录的用户

    def auth(self):
        '''
        username,password 返回登录结果
        :return:
        '''
        count = 0
        while count < 3:
            username = input("username:").strip()
            password = input("password:").strip()
            # Django 使用自带登录认证
            user = authenticate(username=username, password=password)
            # None 代表认证不成功
            # user object ，认证对象 ,user.name
            if not user:
                count += 1          # 登录计数
                print("Invalid username or password!")
            else:
                self.user = user            # 登录成功  user 是一个对象
                return True                 # 必须返回 True
        else:
            print("too many attempts.")     # 错误次数过多

    def start(self):
        """启动交互程序"""

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
                # 让用户选择
                choice = input("select group>:").strip()
                if choice.isdigit():                # 用户输入是数字
                    choice = int(choice)            # 强转
                    host_bind_list = None           # 主机列表
                    if choice >= 0 and choice < len(host_groups):
                        selected_group = host_groups[choice]        # 通过索引取用户选择的组
                        host_bind_list = selected_group.host_user_binds.all()
                    elif choice == len(host_groups):  # 选择的未分组机器
                        # selected_group = self.user.account.host_user_binds.all()
                        host_bind_list = self.user.account.host_user_binds.all()
                    if host_bind_list:
                        while True:                     # 列出主机索引,主机地址
                            for index, host in enumerate(host_bind_list):
                                print("%s.\t%s" % (index, host,))
                            choice2 = input("select host>:").strip()
                            if choice2.isdigit():       # 选择了某台主机
                                choice2 = int(choice2)
                                if choice2 >= 0 and choice2 < len(host_bind_list):
                                    selected_host = host_bind_list[choice2]
                                    print("selected host", selected_host)
                            elif choice2 == 'b':
                                break
