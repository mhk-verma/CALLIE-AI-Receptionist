from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PasswordReset, EmailVerification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model."""
    
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'email_verified', 'onboarding_completed', 'created_at']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'avatar')}),
        ('Role & Status', {'fields': ('role', 'is_active', 'email_verified', 'onboarding_completed')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    """Admin for PasswordReset model."""
    
    list_display = ['user', 'created_at', 'expires_at', 'used']
    list_filter = ['used', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'expires_at']


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """Admin for EmailVerification model."""
    
    list_display = ['user', 'created_at', 'expires_at', 'used']
    list_filter = ['used', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'expires_at']
