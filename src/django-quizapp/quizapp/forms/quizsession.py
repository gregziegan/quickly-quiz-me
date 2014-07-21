from django import forms
from django.forms import ModelForm, Textarea
from quizapp.models import QuizSession

class QuizSessionForm(ModelForm):
    class Meta():
        model = QuizSession
        fields = ['name', 'quiz', 'is_private']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quiz': forms.Select(attrs={'class': 'form-control'}),
        }