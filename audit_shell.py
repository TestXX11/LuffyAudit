__author__ = 'Administrator'

import sys
import os
import django
from audit.backend import user_interactive

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LuffyAudit.settings")  # 设置环境变量 参考manage.py
    django.setup()  # 手动注册django所有的APP

    obj = user_interactive.UserShell(sys.argv)  # 实例化对象
    obj.start()
