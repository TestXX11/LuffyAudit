__author__ = 'Administrator'
import sys,os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LuffyAudit.settings")
import django
from audit.backend import user_welcome
if __name__ == "__main__":
    django.setup()  # 手动注册django所有的APP
    us = user_welcome.UserShell(sys.argv)
    us.welcome()