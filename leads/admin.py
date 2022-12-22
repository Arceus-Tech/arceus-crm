from django.contrib import admin

from .import models

class CommentsInLineAdmin(admin.TabularInline):
    model = models.Comments

class CommentsAdmin(admin.ModelAdmin):
    inlines = [CommentsInLineAdmin]


admin.site.register(models.LeadData, CommentsAdmin)
admin.site.register(models.Status)
admin.site.register(models.Comments)