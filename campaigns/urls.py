from django.urls import path
from . import views

app_name = "campaigns"

urlpatterns = [
path('', views.CampaignsListView.as_view(), name="campaign-list"),
path('create/', views.CampaignsCreateView.as_view(), name="campaign-create"),

]