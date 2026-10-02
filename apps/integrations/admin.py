from django.contrib import admin
from .models import Integration, WebhookLog, AuditLog


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    """Admin for Integration model."""
    
    list_display = ['name', 'business', 'provider', 'status', 'last_sync', 'created_at']
    list_filter = ['provider', 'status', 'created_at']
    search_fields = ['name']
    readonly_fields = ['last_sync', 'created_at', 'updated_at']


@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    """Admin for WebhookLog model."""
    
    list_display = ['business', 'integration', 'event_type', 'status', 'created_at']
    list_filter = ['event_type', 'status', 'created_at']
    search_fields = ['event_type']
    readonly_fields = ['created_at', 'processed_at']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin for AuditLog model."""
    
    list_display = ['user', 'business', 'action', 'model_name', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['model_name', 'object_id']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
