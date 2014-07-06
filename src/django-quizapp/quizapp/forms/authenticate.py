from django.forms import ModelForm
from django import forms
from quizapp.models import QuizUser

class AuthenticationForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField()
    password = forms.CharField()

    class Meta:
        fields = ['email', 'password']