from django.urls import path
from .views import buy_stocks

urlpatterns = [
    path('buy_stocks', buy_stocks, name='buy_stocks'),
]
