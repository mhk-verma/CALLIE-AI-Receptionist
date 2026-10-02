from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, date
from apps.calls.models import Call
from apps.messages.models import Message
from apps.conversations.models import Conversation
from apps.analytics.models import DailyAnalytics


@method_decorator(login_required, name='dispatch')
class AnalyticsView(TemplateView):
    """Analytics dashboard view."""
    template_name = 'analytics/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.businesses.models import Business
        try:
            business = Business.objects.get(owner=self.request.user)
        except Business.DoesNotExist:
            context['no_business'] = True
            return context
        
        # Get date range
        date_range = self.request.GET.get('range', '7')
        today = timezone.now().date()
        
        if date_range == 'today':
            start_date = today
        elif date_range == '7':
            start_date = today - timedelta(days=7)
        elif date_range == '30':
            start_date = today - timedelta(days=30)
        else:
            start_date = today - timedelta(days=7)
        
        # Get analytics data
        analytics_data = DailyAnalytics.objects.filter(
            business=business,
            date__gte=start_date,
            date__lte=today
        ).order_by('date')
        
        # Prepare chart data
        dates = [data.date.strftime('%Y-%m-%d') for data in analytics_data]
        calls = [data.total_calls for data in analytics_data]
        messages = [data.total_messages for data in analytics_data]
        ai_resolved = [data.ai_resolved for data in analytics_data]
        escalated = [data.escalated for data in analytics_data]
        
        # Calculate totals
        total_calls = sum(calls)
        total_messages = sum(messages)
        total_ai_resolved = sum(ai_resolved)
        total_escalated = sum(escalated)
        
        # Get intent analytics
        intent_data = {}
        for conv in Conversation.objects.filter(
            business=business,
            started_at__gte=start_date
        ):
            if conv.customer_intent:
                intent_data[conv.customer_intent] = intent_data.get(conv.customer_intent, 0) + 1
        
        # Get channel analytics
        channel_data = {}
        for msg in Message.objects.filter(
            business=business,
            created_at__gte=start_date
        ):
            channel_data[msg.channel] = channel_data.get(msg.channel, 0) + 1
        
        context.update({
            'business': business,
            'date_range': date_range,
            'chart_data': {
                'dates': dates,
                'calls': calls,
                'messages': messages,
                'ai_resolved': ai_resolved,
                'escalated': escalated,
            },
            'totals': {
                'calls': total_calls,
                'messages': total_messages,
                'ai_resolved': total_ai_resolved,
                'escalated': total_escalated,
            },
            'intent_data': intent_data,
            'channel_data': channel_data,
        })
        
        return context
