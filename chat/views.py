from django.shortcuts import render
from django.http import HttpResponse
from .models import Topic, Room
from .forms import CreateRoom
# Create your views here.

def chats_view(request):
    form = CreateRoom()
    if request.method == 'POST':
        return HttpResponse("ola")
    else:
        return render(request, "chats.html", context={"form": form})