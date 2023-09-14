from django import forms



class BuyStocks(forms.Form):
    stock_symbol = forms.CharField(max_length=10, required=True)
    quantity = forms.IntegerField(required=True)
