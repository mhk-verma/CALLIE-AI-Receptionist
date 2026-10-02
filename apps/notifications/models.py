from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.accounts.models import User
from apps.businesses.models import Business
import uuid


class Notification(models.Model):
    """Notification model for in-app notifications."""
    
    class Type(models.TextChoices):
        URGENT_CALL = 'urgent_call', _('Urgent Call')
        MISSED_CALL = 'missed_call', _('Missed Call')
        NEW_LEAD = 'new_lead', _('New Lead')
        ESCALATED_CONVERSATION = 'escalated_conversation', _('Escalated Conversation')
        IMPORTANT_MESSAGE = 'important_message', _('Important Message')
        SYSTEM = 'system', _('System')

    class Status(models.TextChoices):
        UNREAD = 'unread', _('Unread')
        READ = 'read', _('Read')
        ARCHIVED = 'archived', _('Archived')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=30, choices=Type.choices, verbose_name=_('Type'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    message = models.TextField(verbose_name=_('Message'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNREAD, verbose_name=_('Status'))
    link = models.URLField(blank=True, verbose_name=_('Link'))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_('Metadata'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    read_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Read At'))

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['business', 'created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.email}"

    def mark_as_read(self):
        """Mark notification as read."""
        self.status = self.Status.READ
        self.read_at = timezone.now()
        self.save()


class EmailLog(models.Model):
    """Email log model for tracking sent emails."""
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SENT = 'sent', _('Sent')
        FAILED = 'failed', _('Failed')
        BOUNCED = 'bounced', _('Bounced')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='email_logs')
    to_email = models.EmailField(verbose_name=_('To Email'))
    subject = models.CharField(max_length=255, verbose_name=_('Subject'))
    body = models.TextField(verbose_name=_('Body'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_('Status'))
    error_message = models.TextField(blank=True, verbose_name=_('Error Message'))
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Sent At'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Email Log')
        verbose_name_plural = _('Email Logs')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.to_email}"
