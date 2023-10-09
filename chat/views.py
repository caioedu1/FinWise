from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User
from .forms import CreateRoom, User
from django.db.models import Q
from django.http import HttpResponse
# Create your views here.

def home(request, pk=None):
    room = Room.objects.get(id=pk)
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains= q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)                                  
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    
    context = {'rooms': rooms, 'topics':topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'home.html', context)

from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404

@login_required
def createRoom(request):
    form = CreateRoom()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        if form.is_valid():
            room = form.save(commit=False)
            room.save()
        return redirect('buy_stocks')
        
    context = {'form': form, 'topics':topics}
    return render(request,'chats.html', context)


@login_required
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'room.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = Room(instance=room)
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
    context = {'form':form, 'topics':topics}
    return render(request, 'room_form.html', context)

@login_required
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':room})

@login_required
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':message})


@login_required
def updateUser(request, pk):
    user = request.user
    form = User(instance=user)
    
    if request.method == 'POST':
        form = User(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk= user.id)
    return render(request, 'update_user.html', {'form':form,})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    print(f'Query string received: {q}')  # Debug message

    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'activity.html', {'room_messages':room_messages})