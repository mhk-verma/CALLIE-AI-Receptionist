from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.businesses.models import Business
import uuid


class DailyAnalytics(models.Model):
    """Daily analytics model for aggregated data."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='daily_analytics')
    date = models.DateField(verbose_name=_('Date'))
    
    # Call metrics
    total_calls = models.IntegerField(default=0, verbose_name=_('Total Calls'))
    answered_calls = models.IntegerField(default=0, verbose_name=_('Answered Calls'))
    missed_calls = models.IntegerField(default=0, verbose_name=_('Missed Calls'))
    average_call_duration = models.IntegerField(null=True, blank=True, verbose_name=_('Average Call Duration (seconds)'))
    
    # Message metrics
    total_messages = models.IntegerField(default=0, verbose_name=_('Total Messages'))
    messages_replied = models.IntegerField(default=0, verbose_name=_('Messages Replied'))
    
    # Resolution metrics
    ai_resolved = models.IntegerField(default=0, verbose_name=_('AI Resolved'))
    human_resolved = models.IntegerField(default=0, verbose_name=_('Human Resolved'))
    escalated = models.IntegerField(default=0, verbose_name=_('Escalated'))
    
    # Contact metrics
    new_contacts = models.IntegerField(default=0, verbose_name=_('New Contacts'))
    
    # Urgency metrics
    urgent_flags = models.IntegerField(default=0, verbose_name=_('Urgent Flags'))
    
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_('Metadata'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Daily Analytics')
        verbose_name_plural = _('Daily Analytics')
        unique_together = ['business', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.business.name} - {self.date}"


class IntentAnalytics(models.Model):
    """Intent analytics for tracking customer intents."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='intent_analytics')
    date = models.DateField(verbose_name=_('Date'))
    intent = models.CharField(max_length=255, verbose_name=_('Intent'))
    count = models.IntegerField(default=0, verbose_name=_('Count'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Intent Analytics')
        verbose_name_plural = _('Intent Analytics')
        unique_together = ['business', 'date', 'intent']
        ordering = ['-date', '-count']

    def __str__(self):
        return f"{self.business.name} - {self.intent} - {self.count}"


class ChannelAnalytics(models.Model):
    """Channel analytics for tracking communication channels."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='channel_analytics')
    date = models.DateField(verbose_name=_('Date'))
    channel = models.CharField(max_length=20, verbose_name=_('Channel'))
    count = models.IntegerField(default=0, verbose_name=_('Count'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Channel Analytics')
        verbose_name_plural = _('Channel Analytics')
        unique_together = ['business', 'date', 'channel']
        ordering = ['-date', '-count']

    def __str__(self):
        return f"{self.business.name} - {self.channel} - {self.count}"
