from django.shortcuts import render,redirect, HttpResponse,HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.http import QueryDict

from django.views.generic import TemplateView, ListView, CreateView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from . import models
from . import forms

from agents import models as ag_model

from campaigns import models as cp_model
from campaigns import forms as cp_form

from csv import DictReader

from django.db.models import Q

from datetime import date

import string
import random

from django.utils import timezone

today = date.today()

class LandingPage(TemplateView):
    template_name= 'landing-page.html'


def lead_detail(request, pk):
    lead = get_object_or_404(models.LeadData, pk=pk)
    context = {'lead':lead}

    if request.method == 'GET':
        return render(request, "leads/lead_detail.html", context)
    elif request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = forms.LeadEditModelForm(data, instance=lead)
        if form.is_valid():
            form.save()
            return render(request, "leads/partial/lead-detail.html", context)
        
        context['form'] = form
        return render(request, "leads/partial/lead-edit.html", context)

def lead_edit(request, pk):
    lead = get_object_or_404(models.LeadData, pk=pk)
    form  = forms.LeadEditModelForm(instance=lead)
    context = {'lead':lead, 'form':form}
    return render(request, "leads/partial/lead-edit.html", context)

def update_comment(request, pk):
    user = request.user.email
    lead  = models.LeadData.objects.get(id=pk)

    try:
        agent = ag_model.AgentsInfo.objects.get(user__email=user)
    except:
        agent = ag_model.User.objects.get(user = user)
    
    form = forms.CommentModelForm(data=request.POST or None, user=request.user)

    
    if request.method == "POST":
        if form.is_valid():
            status_t = (form.cleaned_data['status'])

            comment = form.save(commit=False)
            lead.last_updated = timezone.now()
            comment.agent = agent
            comment.lead = lead
            if status_t is None:
                comment.status = lead.status
                lead.status = lead.status
            else:
                lead.status = models.Status.objects.get(pk=(request.POST.get('status')))


            comment.save()
            lead.save()
            return render(request, "leads/comment_list.html",context={
                "comments": reversed(models.Comments.objects.filter(Q(lead=lead)))
            })
        else:
            return render(request, ("leads:lead-list"), context={
                "form": form
            })
    
    context = {
        "form": form,
        "agent": agent,
        "lead": lead,
        "comments": reversed(models.Comments.objects.filter(Q(lead=lead)))
    }

    return render(request, "leads/note_create.html", context)

class CommentsListView(LoginRequiredMixin,ListView):
    template_name = 'leads/lead_comment.html'
    context_object_name = "comment"


class LeadListView(LoginRequiredMixin,ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = "leads"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            queryset = context['leads']
            paginator = Paginator(queryset, self.paginate_by)
            page = self.request.GET.get('page')

            try:
                leads = paginator.page(page)
            except PageNotAnInteger:
                leads = paginator.page(1)
            except EmptyPage:
                leads = paginator.page(paginator.num_pages)

            
            if self.request.user.UserPosition.name == "IT Department" or self.request.user.UserPosition.name == "Compliance":
                status = models.Status.objects.all()
            else:
                status = models.Status.objects.filter( organization = self.request.user.agentsinfo.organization)
                
            
            context['leads'] = leads
            context.update({
                "campaigns": cp_model.Campaigns.objects.all(),
                "campaigns_col": cp_model.CampaignCollection.objects.all(),
                "agents" : ag_model.AgentsInfo.objects.all(),  
                "statuses" : status,  
            })
            return context 
        except:
            pass           

    def get_queryset(self):

        filter  = self.request.GET.get('filter')
        search_post = self.request.GET.get('search')
        campaign_id = self.request.GET.getlist('campaign_id')
        agent_id = self.request.GET.getlist('agent_id')
        note_id = self.request.GET.getlist('note_id')
        user = self.request.user
        print(self.request.user.UserPosition.name )

        if self.request.user.UserPosition.name == "IT Department" or self.request.user.UserPosition.name == "Compliance":
            queryset = models.LeadData.objects.all()
        elif self.request.user.UserPosition.name == "Agent":
            queryset  = models.LeadData.objects.filter( organization = user.agentsinfo.organization)
            queryset = queryset.filter(agent__user=user)
        else:
            organization = ag_model.UserProfile.objects.get(user = user)
            queryset  = models.LeadData.objects.filter( organization = organization)

        if search_post:
            if filter == "id":
                queryset = queryset.filter(Q(lead_name__icontains=search_post))
            elif filter == "email":
                queryset = queryset.filter(Q(email=search_post))
            elif filter == "number":
                queryset = queryset.filter(Q(phone_number__icontains=search_post))
        else:
            if filter:
                if campaign_id:
                    queryset = queryset.filter(Q(campaign_name__in=campaign_id))
            
                if agent_id:
                    if "Unassigned" in agent_id :
                        agent_id.remove("Unassigned")
                        queryset =queryset.filter(Q(agent__isnull=True) | Q(agent__in=agent_id))
                    else:   
                        queryset = queryset.filter(Q(agent__in=agent_id))
                
                if note_id:
                    if "Fresh" in note_id:
                        note_id.remove("Fresh")
                        queryset =queryset.filter(Q(status__isnull=True) | Q(status__in=note_id))
                    else:   
                        queryset = queryset.filter(Q(status__in=note_id))

        return queryset.order_by("pk").reverse()


class LeadCreateView(LoginRequiredMixin, CreateView):
    template_name = 'leads/lead_create.html'
    form_class = forms.LeadModelForm

    def get_success_url(self) -> str:
        return (reverse("leads:lead-list"))


def handle_files(csv_file, name, id, og):
    file_name = f"media/leads/{csv_file}"
    duplicates = []
    with open(file_name, 'r', encoding="utf-8-sig") as read_obj:
        csv_reader = DictReader(read_obj)
        for row in csv_reader:
            lead_name = row['name']
            email = row['email']
            try:
                phone_number = row['number']
            except:
                phone_number = row['phone']
            

            try:
                models.LeadData.objects.create(
                    organization=og,
                    lead_name=lead_name.title(),
                    phone_number= f"+{str(phone_number)}",
                    email=email.lower(),
                    campaign = cp_model.CampaignCollection.objects.get(campaign=id),
                    campaign_name = name
                )
            except Exception as e:
                print(e)
                duplicates.append(row)
                
    return len(duplicates)


def id_generator():
    chars=string.ascii_uppercase + string.digits
    size=6
    final = ''.join(random.choice(chars) for _ in range(size))
    return today.strftime("%b-%d-%Y") + final

def model_form_upload(request):
    if request.method == 'POST':
        form = cp_form.CampaignModelForm(request.POST, request.FILES)
        name = cp_model.Campaigns.objects.get(pk = request.POST["name"])
        og = name.organization
        id = f"{name}-{id_generator()}"

        if form.is_valid():
            test = form.save(commit=False)
            test.campaign = id
            name.last_updated = timezone.now()
            duplicates = handle_files(request.FILES['document'], name, id, og)
            test.duplicates = int((duplicates))

            name.save()
            test.save()
            

            return HttpResponseRedirect(reverse("leads:lead-list") )
    else:
        form = cp_form.CampaignModelForm()
    return render(request, 'leads/lead_upload.html', {
        'form': form
    })



def bulk_assign(request):
    if request.method == "POST":
        lead_ids = request.POST.getlist('lead_id')
        agent_id = request.POST.get('agent_id')
        note_id = request.POST.get("note_id")
        qs = models.LeadData.objects.filter(pk__in = lead_ids)

        if note_id:
            if note_id == "Fresh":
                qs.update(status=None)
            else:
                status = models.Status.objects.get(pk = note_id)
                qs.update(status=status)

        if agent_id:
            if agent_id == "Unassign":
                qs.update(agent=None)
            else:
                try:
                    agent = ag_model.AgentsInfo.objects.get(user__id = agent_id)
                    qs.update(agent=agent)

                except Exception as e:
                    print(e)
                
    return HttpResponseRedirect(reverse("leads:lead-list"))