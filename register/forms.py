from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import password_validation


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
        widgets = {
                'first_name': forms.TextInput(attrs={}),
                'last_name': forms.TextInput(attrs={}),
                'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                'email': forms.EmailInput(attrs={'class': 'form-control', 'aria-describedby': 'emailHelp', 'placeholder': 'Email'}),
                'password1': forms.PasswordInput(attrs={}),
                'password2': forms.PasswordInput(attrs={}),
            }

        
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        
        # Set the placeholder attribute for some fields
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        self.fields['password1'].widget.attrs['class'] = "form-control"
        self.fields['password2'].widget.attrs['class'] = "form-control"     
    
    def clean_password2(self):
        # Retrieve the cleaned data for password1 and password2 fields
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # Run the password validation checks
        try:
            password_validation.validate_password(password2, self.instance)
        except forms.ValidationError as error:
            # Password validation failed, raise the error with a custom message
            raise forms.ValidationError(" ".join(error))

        # Check if the two passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return password2
      
      
class MyUserLoginForm(forms.Form):
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'exampleInputEmail1', 'aria-describedby': 'emailHelp'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'exampleInputPassword1'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'exampleCheck1'}))
    
      
class MyUserUpdateForm(forms.ModelForm):
   class Meta:
      model = User
      fields = ['name', 'username','email', 'avatar', 'bio']
        