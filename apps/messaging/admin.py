from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin for Message model."""
    
    list_display = ['sender_name', 'channel', 'business', 'status', 'urgency', 'direction', 'created_at']
    list_filter = ['channel', 'status', 'urgency', 'direction', 'created_at']
    search_fields = ['sender_name', 'sender_number', 'content']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
