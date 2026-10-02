from django import forms
from .models import FAQ, KnowledgeBaseEntry


class FAQForm(forms.ModelForm):
    """Form for creating/editing FAQs."""

    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'category', 'priority', 'is_active']
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class KnowledgeBaseEntryForm(forms.ModelForm):
    """Form for creating/editing knowledge base entries."""

    class Meta:
        model = KnowledgeBaseEntry
        fields = ['title', 'content', 'category', 'tags', 'is_active', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated tags'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control'}),
        }
