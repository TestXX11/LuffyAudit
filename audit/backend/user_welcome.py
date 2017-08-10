from django.contrib.auth import authenticate
from django.conf import settings
import subprocess
import time

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
            user_host_binds = []
            while True:
                for index,group_name in enumerate(user_host_group):
                    print("%s: %s[%s]"%(index,group_name,group_name.host_user_binds.count()))
                print("%s: %s[%s]" % (len(user_host_group), "未分组",userinfo.account.host_user_binds.count()))
                choices = input("choices HostGroup >>> :").strip()
                if(str(choices).isdigit()):
                    if(int(choices) >= 0 and int(choices) < len(user_host_group)):
                        user_host_binds = user_host_group[int(choices)].host_user_binds.all()
                        # for index,host_name in enumerate(user_host_binds):
                        #     print("%s: %s"%(index,host_name))
                        # choices = input("choices Host >>> :").strip()
                        # if (str(choices).isdigit()):
                        #     if (int(choices) >= 0 and int(choices) < len(group_host)):
                        #         print("you select: %s" % (group_host[int(choices)]))
                    elif(int(choices) == len(user_host_group)):
                        user_host_binds = userinfo.account.host_user_binds.all()
                    if user_host_binds:
                        while True:
                            for index,host_name in enumerate(user_host_binds):
                                print("%s: %s" % (index, host_name))
                            choices = input("choices Host >>> :").strip()
                            if (str(choices).isdigit()):
                                if (int(choices) >= 0 and int(choices) < len(user_host_binds)):
                                    print("you select: %s" % (user_host_binds[int(choices)]))
                                    username = user_host_binds[int(choices)].host_user.username
                                    password = user_host_binds[int(choices)].host_user.password
                                    host_ip = user_host_binds[int(choices)].host.ip_addr
                                    host_port = user_host_binds[int(choices)].host.port

                                    onlyid = time.time()
                                    popen_cmd = "/bin/sh %s %s"%(settings.TRACKER_PATH,onlyid)
                                    res = subprocess.Popen(popen_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                                    cmd = "sshpass -p %s /usr/local/openssh/bin/ssh %s@%s -p %s -Z %s -o StrictHostKeyChecking=no"%(password,username,host_ip,host_port,onlyid)
                                    subprocess.run(cmd,shell=True)
                            elif (choices == "b"):
                                break
                elif(choices=="b"):
                    break



