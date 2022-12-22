from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from agents.models import AgentsInfo, UserProfile
from campaigns.models import Campaigns, CampaignCollection

# LeadData model
class LeadData(models.Model):
    """Lead Information Name, Phone Number, email, date create / update etc..."""
    lead_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey(AgentsInfo, null=True, blank=True , on_delete=models.SET_NULL)
    status = models.ForeignKey("Status", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    campaign_name = models.ForeignKey(Campaigns, null=True, blank=True , on_delete=models.CASCADE)
    campaign = models.ForeignKey(CampaignCollection, null=True, blank=True , on_delete=models.CASCADE)
    
    def __str__(self):
        return (self.lead_name)

class Status(models.Model):
    name = models.CharField(max_length=30)  # New, Contacted, Converted, Unconverted etc...
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Comments(models.Model):

    note = models.TextField()
    agent = models.ForeignKey(AgentsInfo, null=True, blank=True , on_delete=models.SET_NULL)
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
    lead = models.ForeignKey(LeadData, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.note} : {self.agent}" 


