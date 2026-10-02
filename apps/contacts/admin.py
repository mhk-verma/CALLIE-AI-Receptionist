from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin for Contact model."""
    
    list_display = ['name', 'business', 'phone', 'email', 'source', 'is_active', 'created_at']
    list_filter = ['source', 'is_active', 'created_at']
    search_fields = ['name', 'email', 'phone', 'company']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = []  # For tags if using m2m in future
