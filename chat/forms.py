from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
#-----------------------------------------------------#

class CreateRoom(forms.Form):
    name = forms.CharField(required=True, max_length=100)
    description = forms.CharField(required=False, max_length=1000)
