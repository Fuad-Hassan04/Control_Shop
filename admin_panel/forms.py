from django import forms
from .models import customar

class CustomarForm(forms.ModelForm):
    class Meta:
        model = customar
        fields = ['customer_type' , 'name', 'address', 'fhone']
