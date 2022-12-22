from django import forms
from . import models
from agents.models import UserProfile

class CampaignModelForm(forms.ModelForm):
    class Meta:
        model = models.CampaignCollection
        fields = ('name', 'document')

class CampaignCreateModelForm(forms.ModelForm):
    class Meta:
        model = models.Campaigns
        fields = ('name', 'organization', )
    
    def __init__(self, user=None, **kwargs):
        super(CampaignCreateModelForm, self).__init__(**kwargs)
        self.fields['organization'].queryset = UserProfile.objects.filter( user__UserPosition__name__icontains = "leader")
            