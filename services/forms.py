from .models import *
from django import forms

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'image', 'payment_terms', 'price', 'package', 'tax', 'is_active')
 


