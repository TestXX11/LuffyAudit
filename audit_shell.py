__author__ = 'Administrator'

import sys,os
from audit.backend import user_interactive


if __name__ == "__main__":
    #外部py文件执行，需要加"DJANGO_SETTINGS_MODULE", "LuffyAudit.settings"字段
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LuffyAudit.settings")
    import django
    django.setup() #手动注册django所有的APP

    obj = user_interactive.UserShell(sys.argv)
    obj.start()