from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .forms import BuyStocks
import requests
from .models import Stocks
from django.contrib.auth.decorators import login_required
import datetime
import pytz
import urllib
import uuid
import csv

# Create your views here.

@login_required
def buy_stocks(request):
    form = BuyStocks()
    
    if request.method == 'POST':
        form = BuyStocks(request.POST)
        if form.is_valid():
            # api key
            api_key = 'QU6DJSHXR4MROQYO'
            
            # Define stock symbol and quantity
            stock_symbol = form.cleaned_data['stock_symbol']
            quantity = form.cleaned_data['quantity']
            
            end = datetime.datetime.now(pytz.timezone("US/Eastern"))
            start = end - datetime.timedelta(days=7)
            # full url
            url = (
                f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(stock_symbol)}"
                f"?period1={int(start.timestamp())}"
                f"&period2={int(end.timestamp())}"
                f"&interval=1d&events=history&includeAdjustedClose=true"
            )
            
            try:
                response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={"User-Agent": "python-requests", "Accept": "*/*"})
                response.raise_for_status()

                # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
                quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
                quotes.reverse()
                price = round(float(quotes[0]["Adj Close"]), 2)
                if response.status_code == 200:                    
                    purchase_price = price * quantity
                    
                    stock = Stocks(
                        user=request.user,
                        stock_symbol=stock_symbol,
                        quantity=quantity,
                        purchase_price=purchase_price
                    )
                    
                    stock.save()
                    return redirect('buy_stocks')
                else:   
                    return JsonResponse({'error': 'Solicitation error'}, status=400)                
            except (requests.RequestException, ValueError, KeyError, IndexError):
                return JsonResponse({'error': 'Solicitation error'}, status=400)   
            
        else:
            messages.error(request, 'An error has occurred')
    else:
        return render(request, 'stocks/buy_stocks.html', context={'form': form})