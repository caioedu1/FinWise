from django import forms



class BuyStocksForm(forms.Form):
    stock_symbol = forms.CharField(max_length=10, required=True)
    quantity = forms.IntegerField(required=True)

class SellStocksForm(forms.Form):
    stock_symbol = forms.CharField(max_length=10, required=True)
    quantity = forms.IntegerField(required=True)
