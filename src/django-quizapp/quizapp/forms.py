from django.forms.models import modelformset_factory
from django.forms import ModelForm
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(), required=True)