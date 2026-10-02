from django.contrib import admin
from .models import Business, BusinessHours, ReceptionistConfig, EscalationConfig


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    """Admin for Business model."""
    
    list_display = ['name', 'owner', 'business_type', 'phone', 'email', 'is_active', 'created_at']
    list_filter = ['is_active', 'business_type', 'created_at']
    search_fields = ['name', 'owner__email', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    """Admin for BusinessHours model."""
    
    list_display = ['business', 'day', 'is_open', 'open_time', 'close_time']
    list_filter = ['day', 'is_open']
    search_fields = ['business__name']


@admin.register(ReceptionistConfig)
class ReceptionistConfigAdmin(admin.ModelAdmin):
    """Admin for ReceptionistConfig model."""
    
    list_display = ['business', 'name', 'language', 'tone', 'created_at']
    list_filter = ['language', 'tone', 'created_at']
    search_fields = ['business__name', 'name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(EscalationConfig)
class EscalationConfigAdmin(admin.ModelAdmin):
    """Admin for EscalationConfig model."""
    
    list_display = ['business', 'owner_email', 'emergency_contact', 'auto_escalate_on_emergency']
    list_filter = ['auto_escalate_on_emergency', 'created_at']
    search_fields = ['business__name', 'owner_email']
    readonly_fields = ['created_at', 'updated_at']
