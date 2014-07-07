from django import forms
from django.forms import ModelForm, Textarea
from quizapp.models import Question

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        exclude = ['is_deleted']
        widgets = {
            'content': Textarea(attrs={'class': 'form-control'}),
            'ordinal': forms.NumberInput(attrs={'class': 'form-control'}),
            'quiz': forms.Select(attrs={'class': 'form-control'}),
            'answer': Textarea(attrs={'class': 'form-control'}),
        }