from django import forms
from leads.models import AgentsInfo
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import User

class AgentModelForm(forms.ModelForm):
    class Meta:
        model = AgentsInfo
        fields = (
            'user',
            'organization',
        )

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            "last_name",
            "username",
            "email",
            "UserPosition"
        )
        field_classes = {"username": UsernameField}
