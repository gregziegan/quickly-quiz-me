from django import forms
from django.forms import ModelForm, Textarea
from quizapp.models import QuizSession

class QuizSessionForm(ModelForm):
    class Meta():
        model = QuizSession
        fields = ['name', 'quiz']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quiz': forms.Select(attrs={'class': 'form-control'}),
        }