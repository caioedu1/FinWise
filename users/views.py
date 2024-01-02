from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, MyUserLoginForm, MyUserUpdateForm
from .decorators import login_forbidden
from .models import User
from chat.models import Topic
from django.contrib.auth.decorators import login_required


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
            return redirect('home')

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
                return redirect('home')
            else:
                message = 'login failed!'
    return render(request, 'login.html', context={'form':form, 'message': message})


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    avatar_url = user.avatar.url if user.avatar else None
    topics = Topic.objects.all()
    context = {
        'user': user, 
        'rooms':rooms, 
        'topics': topics,
        'room_messages': room_messages,
        'avatar_url': avatar_url,
    }
    return render(request, 'profile.html', context)


@login_required
def updateUser(request, pk):
    user = request.user
    form = MyUserUpdateForm(instance=user)
    
    if request.method == 'POST':
        form = MyUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    return render(request, 'update_user.html', {'form':form})
