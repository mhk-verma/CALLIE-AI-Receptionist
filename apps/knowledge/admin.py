from django.contrib import admin
from .models import FAQ, KnowledgeBaseEntry, Service


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Admin for FAQ model."""
    
    list_display = ['question', 'business', 'category', 'priority', 'is_active', 'view_count']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer']
    readonly_fields = ['view_count', 'created_at', 'updated_at']


@admin.register(KnowledgeBaseEntry)
class KnowledgeBaseEntryAdmin(admin.ModelAdmin):
    """Admin for KnowledgeBaseEntry model."""
    
    list_display = ['title', 'business', 'category', 'priority', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin for Service model."""
    
    list_display = ['name', 'business', 'price', 'duration', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
