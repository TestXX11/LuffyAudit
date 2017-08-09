import sys,os
from audit.backend import user_interactive


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LuffyAudit.settings")   #使用脚本来调用django内置的配置，需要先导入
    import django
    django.setup()   #手动注册django所有的APP

    obj = user_interactive.UserShell(sys.argv)
    obj.start()