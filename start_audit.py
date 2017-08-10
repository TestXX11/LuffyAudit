__author__ = 'Administrator'
import sys,os
if __name__ == "__main__":
    import django
    from audit.backend import user_welcome
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LuffyAudit.settings")
    django.setup()  # 手动注册django所有的APP
    us = user_welcome.UserShell(sys.argv)
    us.welcome()