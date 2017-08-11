from django.contrib import admin
from audit import models
# Register your models here.

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['session','cmd','date']
    list_filter = ['date','session']

class SessionLogAdmin(admin.ModelAdmin):
    list_display = ['id','account','host_user_bind','start_date','end_date']
    list_filter = ['start_date','account']

admin.site.register(models.Host)
admin.site.register(models.HostUser)
admin.site.register(models.HostGroup)
admin.site.register(models.HostUserBind)
admin.site.register(models.Account)
admin.site.register(models.IDC)
<<<<<<< HEAD
admin.site.register(models.AuditLog)
admin.site.register(models.SessionLog)
=======
admin.site.register(models.AuditLog,AuditLogAdmin)
admin.site.register(models.SessionLog,SessionLogAdmin)

>>>>>>> 33d03b7dc5962dd28459f0326df4f90894757d30
