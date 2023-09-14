from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
#-----------------------------------------------------#



class MyUserCreationForm(UserCreationForm):
   class Meta:
      model = User
      fields = ['name', 'username', 'email', 'password1', 'password2']
      
      


class MyUserLoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)
      


            