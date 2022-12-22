from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from leads.views import LandingPage
from agents.views import SignUpView
from campaigns.views import CampaignsListView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name ='landing-page'),
    path('leads/', include('leads.urls', namespace="leads")),
    path('users/', include('agents.urls', namespace="users")),
    path('login/', LoginView.as_view(), name="login-page"),
    path('logout/', LogoutView.as_view(), name="logout-page"),
    path('create/', SignUpView.as_view(), name="create-page"),
    path('campaigns/', include('campaigns.urls', namespace="campaigns")),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)