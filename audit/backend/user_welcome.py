from django.contrib.auth import authenticate
import os,django,sys

class UserShell(object):
    def __init__(self,sys_argv):
        self.sys_argv = sys_argv
        self.user = None

    def welcome(self):
        count=0
        while count < 3:
            username = input("username >>> :").strip()
            password = input("password >>> :").strip()
            userinfo = authenticate(username=username,password=password)
            if not userinfo:
                count+=1
                continue
            user_host_group = userinfo.account.host_groups.all()
            user_host_binds = userinfo.account.host_user_binds.all()
            for index,group_name in enumerate(user_host_group):
                print("%s: %s[%s]"%(index,group_name,group_name.host_user_binds.count()))
            print("%s: %s[%s]" % (len(user_host_group), "未分组",userinfo.account.host_user_binds.count()))
            while True:
                choices = input("choices HostGroup >>> :").strip()
                if(str(choices).isdigit()):
                    if(int(choices) >= 0 and int(choices) < len(user_host_group)):
                        group_host = user_host_group[int(choices)].host_user_binds.all()
                        for index,host_name in enumerate(group_host):
                            print("%s: %s"%(index,host_name))
                        choices = input("choices Host >>> :").strip()
                        if (str(choices).isdigit()):
                            if (int(choices) >= 0 and int(choices) < len(group_host)):
                                print("you select: %s" % (group_host[int(choices)]))

                    elif(int(choices) == len(user_host_group)):
                        for index,host_name in enumerate(user_host_binds):
                            print("%s: %s" % (index, host_name))
                        choices = input("choices Host >>> :").strip()
                        if (str(choices).isdigit()):
                            if (int(choices) >= 0 and int(choices) < len(group_host)):
                                print("you select: %s" % (group_host[int(choices)]))

                elif(choices=="b"):
                    break


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LuffyAudit.settings")
django.setup()#手动注册django所有的APP
us = UserShell(sys.argv)
us.welcome()
