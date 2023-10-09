from django.urls import path
from .views import (createRoom, room, home, 
                    deleteRoom, deleteMessage, 
                    updateRoom, topicsPage,
                    activityPage)


urlpatterns = [
    path('', home, name='home'),
    
    path('chats/room/<int:pk>/', room, name='room'),
    
    path('chats/room/create_room/', createRoom, name='create_room'),
    path('chats/room/update_room/<str:pk>/', updateRoom, name='update_room'),
    path('chats/room/delete_room/<str:pk>/', deleteRoom, name='delete_room'),
    path('chats/room/delete_message/<str:pk>/', deleteMessage, name='delete_message'),

    path('topics/', topicsPage, name='topics'),
    path('activity/', activityPage, name='activity')
]
