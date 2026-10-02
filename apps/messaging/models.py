from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.businesses.models import Business
from apps.contacts.models import Contact
import uuid


class Message(models.Model):
    """Message model for SMS, WhatsApp, Instagram DM, etc."""
    
    class Channel(models.TextChoices):
        SMS = 'sms', _('SMS')
        WHATSAPP = 'whatsapp', _('WhatsApp')
        INSTAGRAM = 'instagram', _('Instagram DM')
        WEBSITE = 'website', _('Website Chat')
        EMAIL = 'email', _('Email')

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SENT = 'sent', _('Sent')
        DELIVERED = 'delivered', _('Delivered')
        READ = 'read', _('Read')
        FAILED = 'failed', _('Failed')

    class Urgency(models.TextChoices):
        NORMAL = 'normal', _('Normal')
        IMPORTANT = 'important', _('Important')
        URGENT = 'urgent', _('Urgent')
        EMERGENCY = 'emergency', _('Emergency')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='channel_messages')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='channel_messages')
    conversation = models.ForeignKey('conversations.Conversation', on_delete=models.SET_NULL, null=True, blank=True, related_name='channel_messages')
    sender_name = models.CharField(max_length=255, blank=True, verbose_name=_('Sender Name'))
    sender_number = models.CharField(max_length=20, blank=True, verbose_name=_('Sender Number'))
    sender_email = models.EmailField(blank=True, verbose_name=_('Sender Email'))
    channel = models.CharField(max_length=20, choices=Channel.choices, verbose_name=_('Channel'))
    content = models.TextField(verbose_name=_('Content'))
    ai_response = models.TextField(blank=True, verbose_name=_('AI Response'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_('Status'))
    urgency = models.CharField(max_length=20, choices=Urgency.choices, default=Urgency.NORMAL, verbose_name=_('Urgency'))
    direction = models.CharField(
        max_length=10,
        choices=[('inbound', 'Inbound'), ('outbound', 'Outbound')],
        default='inbound',
        verbose_name=_('Direction')
    )
    external_id = models.CharField(max_length=255, blank=True, verbose_name=_('External ID'))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_('Metadata'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['business', 'created_at']),
            models.Index(fields=['channel']),
            models.Index(fields=['status']),
            models.Index(fields=['urgency']),
        ]

    def __str__(self):
        return f"{self.get_channel_display()} - {self.sender_name or self.sender_number or 'Unknown'}"
