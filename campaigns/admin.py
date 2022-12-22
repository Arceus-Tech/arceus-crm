from django.contrib import admin

from . import models

class CampaignInLineAdmin(admin.TabularInline):
    model = models.CampaignCollection

class CampaignAdmin(admin.ModelAdmin):
    inlines = [CampaignInLineAdmin]

admin.site.register(models.Campaigns, CampaignAdmin)
admin.site.register(models.CampaignCollection)