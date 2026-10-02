from django.contrib import admin
from .models import Conversation, UrgentFlag, ConversationMessage


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Admin for Conversation model."""
    
    list_display = ['id', 'business', 'contact', 'channel', 'resolution', 'started_at']
    list_filter = ['channel', 'resolution', 'sentiment', 'started_at']
    search_fields = ['summary', 'customer_intent']
    readonly_fields = ['started_at', 'ended_at', 'created_at', 'updated_at']
    date_hierarchy = 'started_at'


@admin.register(UrgentFlag)
class UrgentFlagAdmin(admin.ModelAdmin):
    """Admin for UrgentFlag model."""
    
    list_display = ['conversation', 'level', 'reason', 'is_resolved', 'created_at']
    list_filter = ['level', 'is_resolved', 'created_at']
    search_fields = ['reason']
    readonly_fields = ['created_at']


@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    """Admin for ConversationMessage model."""
    
    list_display = ['conversation', 'sender', 'timestamp']
    list_filter = ['sender', 'timestamp']
    search_fields = ['content']
    readonly_fields = ['timestamp']
