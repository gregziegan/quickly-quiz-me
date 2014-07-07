from django import forms
from django.forms import ModelForm, Textarea
from quizapp.models import Quiz

class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        exclude = ['created_at', 'is_deleted', 'answer_file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'instructions': Textarea(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }