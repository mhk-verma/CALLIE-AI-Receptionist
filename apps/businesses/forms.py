from django import forms
from .models import Business, BusinessHours, ReceptionistConfig, EscalationConfig


class BusinessForm(forms.ModelForm):
    """Form for creating/editing business."""

    class Meta:
        model = Business
        fields = ['name', 'business_type', 'phone', 'email', 'address', 'website', 'description', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_type': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class BusinessHoursForm(forms.ModelForm):
    """Form for business hours."""

    class Meta:
        model = BusinessHours
        fields = ['is_open', 'open_time', 'close_time']
        widgets = {
            'is_open': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'open_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'close_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class ReceptionistConfigForm(forms.ModelForm):
    """Form for AI receptionist configuration."""

    class Meta:
        model = ReceptionistConfig
        fields = ['name', 'personality', 'greeting', 'language', 'tone', 
                  'business_description', 'main_responsibilities', 
                  'max_conversation_length', 'escalation_threshold']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'personality': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'greeting': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'tone': forms.Select(attrs={'class': 'form-control'}),
            'business_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'main_responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'max_conversation_length': forms.NumberInput(attrs={'class': 'form-control'}),
            'escalation_threshold': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class EscalationConfigForm(forms.ModelForm):
    """Form for escalation configuration."""

    class Meta:
        model = EscalationConfig
        fields = ['emergency_contact', 'owner_email', 'urgent_keywords', 
                  'auto_escalate_on_emergency']
        widgets = {
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'urgent_keywords': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'auto_escalate_on_emergency': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
