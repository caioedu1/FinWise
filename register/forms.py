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
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'exampleInputEmail1', 'aria-describedby': 'emailHelp'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'exampleInputPassword1'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'exampleCheck1'}))
      
