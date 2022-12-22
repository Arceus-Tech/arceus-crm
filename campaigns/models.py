from django.db import models

from agents.models import UserProfile

class Campaigns(models.Model):
    name = models.CharField(max_length=150)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    organization = models.ForeignKey(UserProfile,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CampaignCollection(models.Model):
    campaign = models.CharField(max_length=150)
    name = models.ForeignKey(Campaigns, null=True, blank=True , on_delete=models.SET_NULL)
    document = models.FileField(upload_to='leads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    duplicates = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.campaign