from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, MyUserLoginForm



def registerUser(request):
    form = MyUserCreationForm()
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'register/signup.html', context={'form': form}) 


def loginUser(request):
    form = MyUserLoginForm()
    message = ''
    if request.method == 'POST':
        form = MyUserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in!'
                return redirect('register')
            else:
                message = 'login failed!'
    return render(request, 'register/login.html', context={'form':form, 'message': message})


def logoutUser(request):
    logout(request)
    return redirect('login')
