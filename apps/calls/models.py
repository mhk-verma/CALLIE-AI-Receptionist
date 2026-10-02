from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.businesses.models import Business
from apps.contacts.models import Contact
import uuid


class Call(models.Model):
    """Call model representing a phone call."""
    
    class Status(models.TextChoices):
        ANSWERED = 'answered', _('Answered')
        MISSED = 'missed', _('Missed')
        ESCALATED = 'escalated', _('Escalated')
        COMPLETED = 'completed', _('Completed')
        FAILED = 'failed', _('Failed')

    class Urgency(models.TextChoices):
        NORMAL = 'normal', _('Normal')
        IMPORTANT = 'important', _('Important')
        URGENT = 'urgent', _('Urgent')
        EMERGENCY = 'emergency', _('Emergency')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='calls')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='calls')
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone Number'))
    caller_name = models.CharField(max_length=255, blank=True, verbose_name=_('Caller Name'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ANSWERED, verbose_name=_('Status'))
    urgency = models.CharField(max_length=20, choices=Urgency.choices, default=Urgency.NORMAL, verbose_name=_('Urgency'))
    duration = models.IntegerField(null=True, blank=True, help_text='Duration in seconds', verbose_name=_('Duration'))
    recording_url = models.URLField(blank=True, verbose_name=_('Recording URL'))
    transcript = models.TextField(blank=True, verbose_name=_('Transcript'))
    summary = models.TextField(blank=True, verbose_name=_('AI Summary'))
    customer_intent = models.CharField(max_length=255, blank=True, verbose_name=_('Customer Intent'))
    resolution = models.CharField(max_length=100, blank=True, verbose_name=_('Resolution'))
    handled_by = models.CharField(
        max_length=20,
        choices=[('ai', 'AI'), ('human', 'Human')],
        default='ai',
        verbose_name=_('Handled By')
    )
    follow_up_required = models.BooleanField(default=False, verbose_name=_('Follow-up Required'))
    follow_up_notes = models.TextField(blank=True, verbose_name=_('Follow-up Notes'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Call')
        verbose_name_plural = _('Calls')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['business', 'created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['urgency']),
        ]

    def __str__(self):
        return f"Call from {self.phone_number} - {self.status}"


class CallTranscript(models.Model):
    """Call transcript model for storing conversation turn-by-turn."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='transcripts')
    speaker = models.CharField(
        max_length=20,
        choices=[('customer', 'Customer'), ('ai', 'AI Receptionist')],
        verbose_name=_('Speaker')
    )
    content = models.TextField(verbose_name=_('Content'))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Timestamp'))
    confidence_score = models.FloatField(null=True, blank=True, verbose_name=_('Confidence Score'))

    class Meta:
        verbose_name = _('Call Transcript')
        verbose_name_plural = _('Call Transcripts')
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.get_speaker_display()}: {self.content[:50]}..."


class CallAnalytics(models.Model):
    """Call analytics model for storing aggregated call data."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='call_analytics')
    date = models.DateField(verbose_name=_('Date'))
    total_calls = models.IntegerField(default=0, verbose_name=_('Total Calls'))
    answered_calls = models.IntegerField(default=0, verbose_name=_('Answered Calls'))
    missed_calls = models.IntegerField(default=0, verbose_name=_('Missed Calls'))
    escalated_calls = models.IntegerField(default=0, verbose_name=_('Escalated Calls'))
    average_duration = models.IntegerField(null=True, blank=True, verbose_name=_('Average Duration (seconds)'))
    ai_resolved = models.IntegerField(default=0, verbose_name=_('AI Resolved'))
    human_resolved = models.IntegerField(default=0, verbose_name=_('Human Resolved'))

    class Meta:
        verbose_name = _('Call Analytics')
        verbose_name_plural = _('Call Analytics')
        unique_together = ['business', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.business.name} - {self.date}"
