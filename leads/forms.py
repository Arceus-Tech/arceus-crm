from django import forms
from .models import LeadData, Comments
from django.forms import TextInput, EmailInput, NumberInput, Select, Textarea
from . import models

textBoxStyle = "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
selectBoxStyle = "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

class LeadEditModelForm(forms.ModelForm):
    class Meta:
        model = LeadData
        fields = [
            'lead_name',
            'email',
        ]
        widgets = {
            'lead_name': TextInput(attrs={
                'class': textBoxStyle,
                'placeholder': 'PhoneNumber'
            }),
            'email': EmailInput(attrs={
                'class': textBoxStyle,
                'placeholder': 'PhoneNumber'
            })
        }


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = LeadData
        fields = [
            'lead_name',
            'email',
            'phone_number',
            'organization',
            'agent',
            'campaign'
        ]
        widgets = {
            'phone_number': TextInput(attrs={
                'class': textBoxStyle,
                'placeholder': 'PhoneNumber'
            })
        }


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = (
            'status',
            'note',
        )

        widgets = {
            'status': Select(attrs={
                'class': selectBoxStyle,
                'onchange' : "changer(this)"
            }),
            'note': Textarea(attrs={
                'class': textBoxStyle,
                'placeholder': 'Note'
            })
        }
    def __init__(self, user=None, **kwargs):
        super(CommentModelForm, self).__init__(**kwargs)
        if user.UserPosition.name == "IT Department" or user.UserPosition.name == "Compliance":
            self.fields['status'].queryset =  models.Status.objects.all()
        else:
           self.fields['status'].queryset = models.Status.objects.filter( organization = user.agentsinfo.organization)
            