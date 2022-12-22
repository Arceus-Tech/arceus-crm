from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import AgentsInfo, UserProfile
from django.views.generic import ListView, CreateView
from django.urls import reverse
from .forms import AgentModelForm, CustomUserCreationForm



class SignUpView(CreateView):
    template_name= 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return (reverse("login-page"))

class AgentListView(LoginRequiredMixin, ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        position = self.request.user.UserPosition.name

        position_list = ['IT Department', "Compliance", "Sales Leader", "Director"]
        if position in position_list:
            return UserProfile.objects.all()
        else:
            organization = self.request.user.userprofile
            return AgentsInfo.objects.filter(organization=organization)


class AgentCreateView(LoginRequiredMixin, CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("users:agent-list")

    def form_valid(self, form):
        form.save()
        return super(AgentCreateView, self).form_valid(form)
