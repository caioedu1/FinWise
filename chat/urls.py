from django.urls import path
from .views import chats_view

urlpatterns = [
    path('chats', chats_view, name='chats'),
]
