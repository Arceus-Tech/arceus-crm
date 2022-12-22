from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
path('', views.LeadListView.as_view(), name="lead-list"),
path('create/', views.LeadCreateView.as_view(), name="lead-create"),
path('<int:pk>/comments/', views.update_comment,  name="update-comment"),
path('upload/', views.model_form_upload, name="lead-upload"),
path("assign/", views.bulk_assign, name="bulk-assign"),
path('leads/<int:pk>', views.lead_detail, name="lead-detail"),
path('leads/<int:pk>/edit', views.lead_edit, name="lead-edit"),

]