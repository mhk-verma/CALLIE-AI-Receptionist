from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.businesses.models import Business
import uuid


class Contact(models.Model):
    """Contact model representing a customer or lead."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('Phone'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    company = models.CharField(max_length=255, blank=True, verbose_name=_('Company'))
    tags = models.JSONField(default=list, verbose_name=_('Tags'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))
    source = models.CharField(
        max_length=50,
        choices=[
            ('call', 'Call'),
            ('message', 'Message'),
            ('website', 'Website'),
            ('manual', 'Manual'),
            ('import', 'Import'),
        ],
        default='manual',
        verbose_name=_('Source')
    )
    last_interaction = models.DateTimeField(null=True, blank=True, verbose_name=_('Last Interaction'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['business', 'name']),
            models.Index(fields=['business', 'email']),
            models.Index(fields=['business', 'phone']),
        ]

    def __str__(self):
        return f"{self.name} - {self.business.name}"

    def add_tag(self, tag):
        """Add a tag to the contact."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.save()

    def remove_tag(self, tag):
        """Remove a tag from the contact."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.save()
