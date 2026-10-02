from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """Form for creating/editing contacts."""

    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'company', 'tags', 'notes', 'source']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated tags'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'source': forms.Select(attrs={'class': 'form-control'}),
        }
