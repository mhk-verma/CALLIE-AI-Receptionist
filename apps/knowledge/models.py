from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.businesses.models import Business
import uuid


class FAQ(models.Model):
    """FAQ model for frequently asked questions."""
    
    class Category(models.TextChoices):
        GENERAL = 'general', _('General')
        HOURS = 'hours', _('Business Hours')
        PRICING = 'pricing', _('Pricing')
        SERVICES = 'services', _('Services')
        LOCATION = 'location', _('Location')
        PAYMENT = 'payment', _('Payment')
        APPOINTMENT = 'appointment', _('Appointment')
        OTHER = 'other', _('Other')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='faqs')
    question = models.TextField(verbose_name=_('Question'))
    answer = models.TextField(verbose_name=_('Answer'))
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.GENERAL, verbose_name=_('Category'))
    priority = models.IntegerField(default=0, verbose_name=_('Priority'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    view_count = models.IntegerField(default=0, verbose_name=_('View Count'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['-priority', 'created_at']
        indexes = [
            models.Index(fields=['business', 'is_active']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.question[:50]}..."


class KnowledgeBaseEntry(models.Model):
    """Knowledge base entry for business information."""
    
    class Category(models.TextChoices):
        BUSINESS_INFO = 'business_info', _('Business Information')
        SERVICES = 'services', _('Services')
        PRICING = 'pricing', _('Pricing')
        POLICIES = 'policies', _('Policies')
        HOURS = 'hours', _('Opening Hours')
        CONTACT = 'contact', _('Contact Information')
        LOCATIONS = 'locations', _('Locations')
        SPECIAL_INSTRUCTIONS = 'special_instructions', _('Special Instructions')
        OTHER = 'other', _('Other')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='knowledge_entries')
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    content = models.TextField(verbose_name=_('Content'))
    category = models.CharField(max_length=30, choices=Category.choices, verbose_name=_('Category'))
    tags = models.JSONField(default=list, blank=True, verbose_name=_('Tags'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    priority = models.IntegerField(default=0, verbose_name=_('Priority'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Knowledge Base Entry')
        verbose_name_plural = _('Knowledge Base Entries')
        ordering = ['-priority', 'created_at']
        indexes = [
            models.Index(fields=['business', 'is_active']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title


class Service(models.Model):
    """Service model for business services."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255, verbose_name=_('Service Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Price'))
    duration = models.IntegerField(null=True, blank=True, help_text='Duration in minutes', verbose_name=_('Duration'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.business.name}"
