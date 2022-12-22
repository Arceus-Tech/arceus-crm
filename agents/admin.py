from django.contrib import admin

from . import models

class RemainderInLineAdmin(admin.TabularInline):
    model = models.CallBackRemainder

class RemaindersAdmin(admin.ModelAdmin):
    inlines = [RemainderInLineAdmin]

admin.site.register(models.User, RemaindersAdmin)
admin.site.register(models.CallBackRemainder)
admin.site.register(models.UserProfile)
admin.site.register(models.UserPosition)
admin.site.register(models.AgentsInfo)