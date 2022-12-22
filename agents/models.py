from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache  
import datetime
from crm import settings
 
class UserPosition(models.Model):
    """Represents the user positions like Directors, IT, Agents etc..."""
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """User Model adding position"""
    UserPosition = models.ForeignKey(
        UserPosition,
        related_name="user_position",
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    
    last_online = models.DateTimeField(blank=True, null=True)
 

class CallBackRemainder(models.Model):
    remainder_time = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Lead_id = models.IntegerField(default=0)


class UserProfile(models.Model):

    """Represents the profile where the user is admitted,
    Classifying leads accordingly"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
        )
    def __str__(self):
        return self.user.username
    
    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                        seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False 



class AgentsInfo (models.Model):
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email



def post_user_created_signal(sender, instance, created, **kwargs):

    """Simulates the user profile action automatically
    when the user is created"""
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)


