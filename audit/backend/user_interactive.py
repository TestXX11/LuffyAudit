__author__ = 'Administrator'
from django.contrib.auth import authenticate
import getpass


class UserShell(object):
    """用户登录堡垒机后的shell"""

    def __init__(self, sys_argv):
        self.sys_argv = sys_argv
        self.user = None

    def auth(self):

        count = 0
        while count < 3:
            username = input("username:").strip()
            password = getpass.getpass("password:").strip()  # 输入密码不可见
            user = authenticate(username=username, password=password)  # authenticate 是Django的的验证
            # None 代表认证不成功
            # user object ，认证对象 ,user.name
            if not user:
                count += 1
                print("Invalid username or password!")
            else:
                self.user = user
                return True
        else:
            print("too many attempts.")

    def start(self):
        """启动交互程序"""

        if self.auth():
            # print(self.user.account.host_user_binds.all()) #select_related()
            while True:
                host_groups = self.user.account.host_groups.all() # 通过user对象从account表中获取主机表中的数据
                for index, group in enumerate(host_groups):
                    print("%s.\t%s[%s]" % (index, group, group.host_user_binds.count())) # 通过group获取分组中的数量
                print("%s.\t未分组机器[%s]" % (len(host_groups), self.user.account.host_user_binds.count())) # 从account中获取没有分组的主机

                choice = input("select group>:").strip()
                if choice.isdigit():
                    choice = int(choice)
                    host_bind_list = None
                    if choice >= 0 and choice < len(host_groups): # 选择的边界
                        selected_group = host_groups[choice]
                        host_bind_list = selected_group.host_user_binds.all() # 从主机组或者未分组的数据中 查看选中的数据
                    elif choice == len(host_groups):  # 选择的未分组机器
                        # selected_group = self.user.account.host_user_binds.all()
                        host_bind_list = self.user.account.host_user_binds.all()
                    if host_bind_list:
                        while True:
                            for index, host in enumerate(host_bind_list):
                                print("%s.\t%s" % (index, host,))
                            choice2 = input("select host>:").strip()
                            if choice2.isdigit():
                                choice2 = int(choice2)
                                if choice2 >= 0 and choice2 < len(host_bind_list):
                                    selected_host = host_bind_list[choice2]
                                    print("selected host", selected_host)
                            elif choice2 == 'b':
                                break
