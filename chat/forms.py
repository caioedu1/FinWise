from .models import User, Room
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from .models import Topic

#-----------------------------------------------------#


class CreateRoom(ModelForm):
     class Meta:
        model = Room
        fields = ['topic', 'name', 'description']