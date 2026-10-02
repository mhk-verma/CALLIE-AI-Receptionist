from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    """Main dashboard view."""
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['stats'] = {
            'calls_today': 0,
            'messages_today': 0,
            'missed_calls': 0,
            'urgent_issues': 0,
            'new_contacts': 0,
            'ai_resolved': 0,
            'escalated': 0,
            'customer_satisfaction': 98,
        }
        
        context['recent_activity'] = []
        context['business'] = None
        
        return context
