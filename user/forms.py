from .models import *
from django import forms

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('fullname', 'email', 'mobile', 'address', 'password')



