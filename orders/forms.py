from django import forms
from .models import Order, ProductInOrder

class CheckContactForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'

class ProductInOrderForm(forms.ModelForm):

    class Meta:
        model = ProductInOrder
        fields = ['product', 'nmb']
