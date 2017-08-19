#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from django.contrib import admin
from audit import models


# Register your models here.
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['session', 'cmd', 'date', ]
    lsit_filter = ['date', 'session']


class SessionLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'host_user_bind', 'start_date', 'end_date']
    lsit_filter = ['start_date', 'account']

class TaskLogAdmin(admin.ModelAdmin):
    list_display = ['id','task_id','host_user_bind_id', 'result','date' ]
    list_filter = ['result',]

admin.site.register(models.Host)
admin.site.register(models.HostUser)
admin.site.register(models.HostGroup)
admin.site.register(models.HostUserBind)
admin.site.register(models.Account)
admin.site.register(models.IDC)
admin.site.register(models.AuditLog, AuditLogAdmin)
admin.site.register(models.SessionLog, SessionLogAdmin)
admin.site.register(models.Task)
admin.site.register(models.Token)
admin.site.register(models.TaskLog,TaskLogAdmin)
