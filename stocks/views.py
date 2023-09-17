from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .forms import BuyStocksForm, SellStocksForm
import requests
from .models import BuyStocks, SellStocks, UsersStocks
from register.models import User
from django.contrib.auth.decorators import login_required
import datetime
import pytz
import urllib
import uuid
import csv
from decimal import Decimal

# Create your views here.


@login_required
def buy_stocks(request):
    form = BuyStocksForm()

    if request.method == "POST":
        form = BuyStocksForm(request.POST)
        user_id = request.user.id

        if form.is_valid():
            # Define stock symbol and quantity
            stock_symbol = form.cleaned_data["stock_symbol"]
            stock_symbol = stock_symbol.upper()
            quantity = form.cleaned_data["quantity"]

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
                response = requests.get(
                    url,
                    cookies={"session": str(uuid.uuid4())},
                    headers={"User-Agent": "python-requests", "Accept": "*/*"},
                )
                response.raise_for_status()

                # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
                quotes = list(
                    csv.DictReader(response.content.decode("utf-8").splitlines())
                )
                quotes.reverse()
                price = round(float(quotes[0]["Adj Close"]), 2)
                if response.status_code == 200:
                    purchase_price = Decimal(str(price)) * quantity

                    stock = BuyStocks(
                        user=request.user,
                        stock_symbol=stock_symbol,
                        quantity=quantity,
                        purchase_price=purchase_price,
                    )

                    stock.save()

                    # Update users stocks table
                    existing_stock = UsersStocks.objects.filter(
                        user_id=user_id, stock_symbol=stock_symbol
                    ).first()
                    user = User.objects.get(id=user_id)

                    if purchase_price > user.cash:
                        return HttpResponse("You do not have enough money")
                    
                    if existing_stock:
                        existing_stock.quantity += quantity
                        existing_stock.save()
                    else:
                        new_stock = UsersStocks(
                            user_id=user_id,
                            stock_symbol=stock_symbol,
                            quantity=quantity,
                        )
                        new_stock.save()

                    user.cash -= purchase_price
                    user.save()

                    return redirect("buy_stocks")
                else:
                    return JsonResponse({"error": "Solicitation error"}, status=400)
            except (requests.RequestException, ValueError, KeyError, IndexError):
                return JsonResponse({"error": "Solicitation error"}, status=400)
        else:
            messages.error(request, "An error has occurred")
    else:
        return render(request, "buy_stocks.html", context={"form": form})


@login_required
def sell_stocks(request):
    form = SellStocksForm()

    if request.method == "POST":
        form = SellStocksForm(request.POST)
        user_id = request.user.id

        if form.is_valid():
            # api key
            api_key = "QU6DJSHXR4MROQYO"

            # Define stock symbol and quantity
            stock_symbol = form.cleaned_data["stock_symbol"]
            stock_symbol = stock_symbol.upper()
            quantity = form.cleaned_data["quantity"]

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
                response = requests.get(
                    url,
                    cookies={"session": str(uuid.uuid4())},
                    headers={"User-Agent": "python-requests", "Accept": "*/*"},
                )
                response.raise_for_status()

                # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
                quotes = list(
                    csv.DictReader(response.content.decode("utf-8").splitlines())
                )
                quotes.reverse()
                price = round(float(quotes[0]["Adj Close"]), 2)
                if response.status_code == 200:
                    sale_price = Decimal(str(price)) * quantity

                    stock = SellStocks(
                        user=request.user,
                        stock_symbol=stock_symbol,
                        quantity=quantity,
                        sale_price=sale_price,
                    )

                    stock.save()

                    # Handling selling table and updating users stocks table
                    existing_stock = UsersStocks.objects.filter(
                        user_id=user_id, stock_symbol=stock_symbol
                    ).first()

                    if not existing_stock:
                        return HttpResponse("You do not have this stock")
                    if existing_stock.quantity < quantity:
                        return HttpResponse("You do not have that quantity of stocks")

                    existing_stock.quantity -= quantity
                    existing_stock.save()

                    user = User.objects.get(id=user_id)
                    user.cash += sale_price
                    user.save()

                    return redirect("sell_stocks")
                else:
                    return JsonResponse({"error": "Solicitation error"}, status=400)
            except (requests.RequestException, ValueError, KeyError, IndexError):
                return JsonResponse({"error": "Solicitation error"}, status=400)
        else:
            messages.error(request, "An error has occurred")
    else:
        return render(request, "sell_stocks.html", context={"form": form})
