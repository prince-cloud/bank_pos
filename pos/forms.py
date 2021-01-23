from django import forms
from . import models

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = models.Purchase
        fields = ("product", "quantity", "price")


class SupplyForm(forms.ModelForm):
    class Meta:
        model = models.Supply
        fields = ('product', 'quantity')


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields  = ('name', 'available_quantity', 'description')


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = models.Expense
        fields = ('description', 'amount')
