from django.contrib import admin
from .models import Notification, EmailLog


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin for Notification model."""
    
    list_display = ['user', 'business', 'type', 'title', 'status', 'created_at']
    list_filter = ['type', 'status', 'created_at']
    search_fields = ['title', 'message']
    readonly_fields = ['created_at', 'read_at']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    """Admin for EmailLog model."""
    
    list_display = ['business', 'to_email', 'subject', 'status', 'sent_at', 'created_at']
    list_filter = ['status', 'sent_at', 'created_at']
    search_fields = ['to_email', 'subject']
    readonly_fields = ['created_at']
