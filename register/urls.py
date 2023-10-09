from django.contrib import admin
from django.urls import path
from .views import registerUser, loginUser, logoutUser, userProfile

urlpatterns = [
    path('register', registerUser, name='register'),
    path('login', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    
    path('user_profile/<str:pk>/', userProfile, name='user_profile')
]

