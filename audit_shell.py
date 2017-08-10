__author__ = 'Administrator'

import sys, os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jackupdownAudit.settings")
    import django

    django.setup()  # 手动注册django所有的APP

    from audit.backend import user_interactive  # 由于user_interactive用到了django的表，所以需要在django设置后导入

    obj = user_interactive.UserShell(sys.argv)
    obj.start()
