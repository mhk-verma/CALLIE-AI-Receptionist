from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.businesses.models import Business
from apps.contacts.models import Contact
import uuid


class Conversation(models.Model):
    """Conversation model representing a complete interaction."""
    
    class Channel(models.TextChoices):
        CALL = 'call', _('Call')
        SMS = 'sms', _('SMS')
        WHATSAPP = 'whatsapp', _('WhatsApp')
        INSTAGRAM = 'instagram', _('Instagram DM')
        WEBSITE = 'website', _('Website Chat')
        EMAIL = 'email', _('Email')

    class Resolution(models.TextChoices):
        AI_RESOLVED = 'ai_resolved', _('AI Resolved')
        ESCALATED = 'escalated', _('Escalated')
        HUMAN_RESOLVED = 'human_resolved', _('Human Resolved')
        PENDING = 'pending', _('Pending')
        ABANDONED = 'abandoned', _('Abandoned')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='conversations')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
    channel = models.CharField(max_length=20, choices=Channel.choices, verbose_name=_('Channel'))
    summary = models.TextField(blank=True, verbose_name=_('AI Summary'))
    customer_intent = models.CharField(max_length=255, blank=True, verbose_name=_('Customer Intent'))
    resolution = models.CharField(max_length=20, choices=Resolution.choices, default=Resolution.PENDING, verbose_name=_('Resolution'))
    sentiment = models.CharField(
        max_length=20,
        choices=[
            ('positive', 'Positive'),
            ('neutral', 'Neutral'),
            ('negative', 'Negative'),
        ],
        blank=True,
        verbose_name=_('Sentiment')
    )
    follow_up_required = models.BooleanField(default=False, verbose_name=_('Follow-up Required'))
    follow_up_notes = models.TextField(blank=True, verbose_name=_('Follow-up Notes'))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_('Metadata'))
    started_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Started At'))
    ended_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Ended At'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversations')
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['business', 'started_at']),
            models.Index(fields=['channel']),
            models.Index(fields=['resolution']),
        ]

    def __str__(self):
        return f"Conversation {self.id} - {self.get_channel_display()}"


class UrgentFlag(models.Model):
    """Urgent flag model for marking urgent conversations."""
    
    class Level(models.TextChoices):
        NORMAL = 'normal', _('Normal')
        IMPORTANT = 'important', _('Important')
        URGENT = 'urgent', _('Urgent')
        EMERGENCY = 'emergency', _('Emergency')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='urgent_flags')
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.URGENT, verbose_name=_('Level'))
    reason = models.TextField(verbose_name=_('Reason'))
    keywords_detected = models.JSONField(default=list, blank=True, verbose_name=_('Keywords Detected'))
    is_resolved = models.BooleanField(default=False, verbose_name=_('Is Resolved'))
    resolved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Resolved By'))
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Resolved At'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Urgent Flag')
        verbose_name_plural = _('Urgent Flags')
        ordering = ['-created_at']

    def __str__(self):
        return f"Urgent Flag - {self.get_level_display()}"


class ConversationMessage(models.Model):
    """Individual message within a conversation."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='conversation_messages')
    sender = models.CharField(
        max_length=20,
        choices=[('customer', 'Customer'), ('ai', 'AI Receptionist'), ('human', 'Human')],
        verbose_name=_('Sender')
    )
    content = models.TextField(verbose_name=_('Content'))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Timestamp'))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_('Metadata'))

    class Meta:
        verbose_name = _('Conversation Message')
        verbose_name_plural = _('Conversation Messages')
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.get_sender_display()}: {self.content[:50]}..."
