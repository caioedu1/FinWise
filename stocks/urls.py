from django.urls import path
from .views import buy_stocks, sell_stocks

urlpatterns = [
    path('buy_stocks', buy_stocks, name='buy_stocks'),
    path('sell_stocks', sell_stocks, name='sell_stocks')
]
