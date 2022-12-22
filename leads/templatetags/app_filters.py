from django import template
from leads.models import LeadData
from campaigns.models import CampaignCollection, Campaigns
register = template.Library()

@register.filter(name='sub')
def sub(value, arg):
    return value - arg + 1

@register.filter(name='count_leads')
def count_leads(value):
    set = LeadData.objects.filter( campaign_name = value)
    return (len(set))    

@register.filter(name='count_unassign_leads')
def count_unassign_leads(value):
    set = LeadData.objects.filter(campaign_name = value)
    set = set.filter(agent = None)
    return (len(set))  

@register.filter(name='count_duplicates')
def count_duplicates(value):
    set = CampaignCollection.objects.filter(name = value)
    duplicate = 0
    for items in set:
        duplicate += items.duplicates
     
    return duplicate


@register.filter(name='agent_check')
def agent_check(value, arg):

    if (int(value)) == int(arg):
        return True
    else:
        False