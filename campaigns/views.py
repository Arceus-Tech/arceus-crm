from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView
from . import models
from .forms import CampaignModelForm, CampaignCreateModelForm
from django.urls import reverse

class CampaignsListView(LoginRequiredMixin,ListView):
    template_name = 'campaigns/campaign_list.html'
    context_object_name = "campaigns"
    model = models.Campaigns

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "campaigns_col": models.CampaignCollection.objects.all(),

        })
        return context 


class CampaignsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'campaigns/campaign_create.html'
    form_class = CampaignCreateModelForm

    def get_success_url(self) -> str:
        return (reverse("campaigns:campaign-list"))