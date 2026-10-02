from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


@method_decorator(login_required, name='dispatch')
class DemoHomeView(TemplateView):
    """Demo home page."""
    template_name = 'demo/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_business'] = True
        context['receptionist'] = {
            'name': 'Callie',
            'get_formatted_greeting': 'Hello! Thank you for calling. My name is Callie, your virtual receptionist. How can I help you today?'
        }
        context['channels'] = {
            'sms': 'SMS',
            'whatsapp': 'WhatsApp',
            'instagram': 'Instagram',
            'website': 'Website Chat'
        }
        return context


@method_decorator(login_required, name='dispatch')
class SimulateCallView(TemplateView):
    """Simulate a phone call."""
    template_name = 'demo/simulate_call.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['receptionist'] = {
            'name': 'Callie',
            'get_formatted_greeting': 'Hello! Thank you for calling. My name is Callie, your virtual receptionist. How can I help you today?'
        }
        return context
