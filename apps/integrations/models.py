from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.businesses.models import Business
import uuid


class Integration(models.Model):
    """Integration model for external services."""
    
    class Provider(models.TextChoices):
        TWILIO = 'twilio', _('Twilio')
        SENDGRID = 'sendgrid', _('SendGrid')
        STRIPE = 'stripe', _('Stripe')
        ZAPIER = 'zapier', _('Zapier')
        CUSTOM = 'custom', _('Custom')

    class Status(models.TextChoices):
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')
        ERROR = 'error', _('Error')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='integrations')
    provider = models.CharField(max_length=20, choices=Provider.choices, verbose_name=_('Provider'))
    name = models.CharField(max_length=255, verbose_name=_('Integration Name'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INACTIVE, verbose_name=_('Status'))
    config = models.JSONField(default=dict, verbose_name=_('Configuration'))
    webhook_url = models.URLField(blank=True, verbose_name=_('Webhook URL'))
    last_sync = models.DateTimeField(null=True, blank=True, verbose_name=_('Last Sync'))
    error_message = models.TextField(blank=True, verbose_name=_('Error Message'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Integration')
        verbose_name_plural = _('Integrations')
        ordering = ['-created_at']
        unique_together = ['business', 'provider']

    def __str__(self):
        return f"{self.name} - {self.get_provider_display()}"


class WebhookLog(models.Model):
    """Webhook log model for tracking incoming webhooks."""
    
    class Status(models.TextChoices):
        SUCCESS = 'success', _('Success')
        FAILED = 'failed', _('Failed')
        PENDING = 'pending', _('Pending')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='webhook_logs')
    integration = models.ForeignKey(Integration, on_delete=models.SET_NULL, null=True, blank=True, related_name='webhook_logs')
    event_type = models.CharField(max_length=100, verbose_name=_('Event Type'))
    payload = models.JSONField(verbose_name=_('Payload'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_('Status'))
    response_code = models.IntegerField(null=True, blank=True, verbose_name=_('Response Code'))
    response_body = models.TextField(blank=True, verbose_name=_('Response Body'))
    error_message = models.TextField(blank=True, verbose_name=_('Error Message'))
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Processed At'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Webhook Log')
        verbose_name_plural = _('Webhook Logs')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event_type} - {self.status}"


class AuditLog(models.Model):
    """Audit log model for tracking system actions."""
    
    class Action(models.TextChoices):
        CREATE = 'create', _('Create')
        UPDATE = 'update', _('Update')
        DELETE = 'delete', _('Delete')
        LOGIN = 'login', _('Login')
        LOGOUT = 'logout', _('Logout')
        VIEW = 'view', _('View')
        EXPORT = 'export', _('Export')
        IMPORT = 'import', _('Import')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=Action.choices, verbose_name=_('Action'))
    model_name = models.CharField(max_length=100, verbose_name=_('Model Name'))
    object_id = models.CharField(max_length=255, blank=True, verbose_name=_('Object ID'))
    changes = models.JSONField(default=dict, blank=True, verbose_name=_('Changes'))
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name=_('IP Address'))
    user_agent = models.TextField(blank=True, verbose_name=_('User Agent'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['business', 'created_at']),
            models.Index(fields=['action']),
        ]

    def __str__(self):
        return f"{self.get_action_display()} - {self.model_name}"
