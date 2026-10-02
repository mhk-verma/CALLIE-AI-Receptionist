from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
import uuid


class Business(models.Model):
    """Business model representing a company using the AI receptionist."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=255, verbose_name=_('Business Name'))
    business_type = models.CharField(max_length=100, verbose_name=_('Business Type'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone Number'))
    email = models.EmailField(verbose_name=_('Email'))
    address = models.TextField(blank=True, verbose_name=_('Address'))
    website = models.URLField(blank=True, verbose_name=_('Website'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True, verbose_name=_('Logo'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Business')
        verbose_name_plural = _('Businesses')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class BusinessHours(models.Model):
    """Business hours model."""
    
    class Day(models.TextChoices):
        MONDAY = 'monday', _('Monday')
        TUESDAY = 'tuesday', _('Tuesday')
        WEDNESDAY = 'wednesday', _('Wednesday')
        THURSDAY = 'thursday', _('Thursday')
        FRIDAY = 'friday', _('Friday')
        SATURDAY = 'saturday', _('Saturday')
        SUNDAY = 'sunday', _('Sunday')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='business_hours')
    day = models.CharField(max_length=10, choices=Day.choices, verbose_name=_('Day'))
    is_open = models.BooleanField(default=True, verbose_name=_('Is Open'))
    open_time = models.TimeField(blank=True, null=True, verbose_name=_('Open Time'))
    close_time = models.TimeField(blank=True, null=True, verbose_name=_('Close Time'))

    class Meta:
        verbose_name = _('Business Hours')
        verbose_name_plural = _('Business Hours')
        unique_together = ['business', 'day']
        ordering = ['day']

    def __str__(self):
        return f"{self.business.name} - {self.get_day_display()}"


class ReceptionistConfig(models.Model):
    """AI Receptionist configuration model."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='receptionist_config')
    name = models.CharField(max_length=100, default='Callie', verbose_name=_('Receptionist Name'))
    personality = models.TextField(
        default='Friendly, professional and concise.',
        verbose_name=_('Personality')
    )
    greeting = models.TextField(
        default='Hello! Thank you for calling. My name is {name}, your virtual receptionist. How can I help you today?',
        verbose_name=_('Greeting')
    )
    language = models.CharField(max_length=10, default='en', verbose_name=_('Language'))
    tone = models.CharField(
        max_length=50,
        choices=[
            ('formal', 'Formal'),
            ('casual', 'Casual'),
            ('friendly', 'Friendly'),
            ('professional', 'Professional'),
        ],
        default='professional',
        verbose_name=_('Tone')
    )
    business_description = models.TextField(blank=True, verbose_name=_('Business Description'))
    main_responsibilities = models.TextField(
        blank=True,
        help_text='List the main responsibilities of the AI receptionist',
        verbose_name=_('Main Responsibilities')
    )
    max_conversation_length = models.IntegerField(
        default=10,
        help_text='Maximum number of turns in a conversation',
        verbose_name=_('Max Conversation Length')
    )
    escalation_threshold = models.IntegerField(
        default=3,
        help_text='Number of failed attempts before escalating',
        verbose_name=_('Escalation Threshold')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Receptionist Config')
        verbose_name_plural = _('Receptionist Configs')

    def __str__(self):
        return f"{self.business.name} - {self.name}"

    def get_formatted_greeting(self):
        """Return greeting with receptionist name inserted."""
        return self.greeting.format(name=self.name)


class EscalationConfig(models.Model):
    """Escalation configuration model."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='escalation_config')
    emergency_contact = models.CharField(max_length=20, blank=True, verbose_name=_('Emergency Contact'))
    owner_email = models.EmailField(verbose_name=_('Owner Email'))
    notification_preferences = models.JSONField(
        default=dict,
        help_text='JSON object with notification preferences',
        verbose_name=_('Notification Preferences')
    )
    urgent_keywords = models.TextField(
        default='emergency,urgent,immediately,critical,accident,cannot wait',
        help_text='Comma-separated list of urgent keywords',
        verbose_name=_('Urgent Keywords')
    )
    escalation_rules = models.JSONField(
        default=dict,
        help_text='JSON object with escalation rules',
        verbose_name=_('Escalation Rules')
    )
    auto_escalate_on_emergency = models.BooleanField(
        default=True,
        verbose_name=_('Auto Escalate on Emergency')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Escalation Config')
        verbose_name_plural = _('Escalation Configs')

    def __str__(self):
        return f"{self.business.name} - Escalation Config"

    def get_urgent_keywords_list(self):
        """Return urgent keywords as a list."""
        return [kw.strip().lower() for kw in self.urgent_keywords.split(',')]
