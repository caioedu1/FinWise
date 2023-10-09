from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, MyUserLoginForm
from django.http import HttpResponse
from .decorators import login_forbidden
from .models import User
from chat.models import Topic


@login_forbidden
def registerUser(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.add_message(request, constants.ERROR, "Email already registered")

            user = form.save(commit=False)
            user.username = user.username.lower()
            user.backend = 'register.backends.EmailBackend'
            user.save()
            login(request, user)

    return render(request, 'signup.html', context={'form': form, 'messages': messages.get_messages(request)})


@login_forbidden
def loginUser(request):
    form = MyUserLoginForm()
    message = ''
    if request.method == 'POST':
        form = MyUserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in!'
                return redirect('register')
            else:
                message = 'login failed!'
    return render(request, 'login.html', context={'form':form, 'message': message})


def logoutUser(request):
    logout(request)
    return redirect('login')


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms':rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)
