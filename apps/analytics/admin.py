from django.contrib import admin
from .models import DailyAnalytics, IntentAnalytics, ChannelAnalytics


@admin.register(DailyAnalytics)
class DailyAnalyticsAdmin(admin.ModelAdmin):
    """Admin for DailyAnalytics model."""
    
    list_display = ['business', 'date', 'total_calls', 'total_messages', 'ai_resolved', 'escalated']
    list_filter = ['date']
    readonly_fields = ['date', 'created_at', 'updated_at']


@admin.register(IntentAnalytics)
class IntentAnalyticsAdmin(admin.ModelAdmin):
    """Admin for IntentAnalytics model."""
    
    list_display = ['business', 'date', 'intent', 'count']
    list_filter = ['date', 'intent']
    readonly_fields = ['created_at']


@admin.register(ChannelAnalytics)
class ChannelAnalyticsAdmin(admin.ModelAdmin):
    """Admin for ChannelAnalytics model."""
    
    list_display = ['business', 'date', 'channel', 'count']
    list_filter = ['date', 'channel']
    readonly_fields = ['created_at']
