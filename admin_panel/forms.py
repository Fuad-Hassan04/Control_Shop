from django import forms
from .models import *

class CustomarForm(forms.ModelForm):
    class Meta:
        model = customar
        fields = ['customer_type' , 'name', 'address', 'fhone']

class AddDetailForm(forms.ModelForm):
    class Meta:
        model = customar_ditail
        fields = [ 'buy_product', 'given_money', 'get_money','total_amount']
