from django.contrib import admin
from .models import Call, CallTranscript, CallAnalytics


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    """Admin for Call model."""
    
    list_display = ['phone_number', 'caller_name', 'business', 'status', 'urgency', 'handled_by', 'created_at']
    list_filter = ['status', 'urgency', 'handled_by', 'created_at']
    search_fields = ['phone_number', 'caller_name', 'summary']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(CallTranscript)
class CallTranscriptAdmin(admin.ModelAdmin):
    """Admin for CallTranscript model."""
    
    list_display = ['call', 'speaker', 'timestamp']
    list_filter = ['speaker', 'timestamp']
    search_fields = ['content']
    readonly_fields = ['timestamp']


@admin.register(CallAnalytics)
class CallAnalyticsAdmin(admin.ModelAdmin):
    """Admin for CallAnalytics model."""
    
    list_display = ['business', 'date', 'total_calls', 'answered_calls', 'missed_calls']
    list_filter = ['date']
    readonly_fields = ['date']
