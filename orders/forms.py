from django import forms

class CheckContactForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)