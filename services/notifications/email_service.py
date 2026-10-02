"""
Email service for sending notifications.
"""
from typing import Optional, List
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails."""
    
    def __init__(self):
        self.from_email = settings.DEFAULT_FROM_EMAIL
    
    def send_urgent_alert(
        self,
        to_email: str,
        business_name: str,
        urgency_level: str,
        reason: str,
        conversation_id: str
    ) -> bool:
        """Send urgent alert email."""
        subject = f"URGENT: {urgency_level.upper()} Alert - {business_name}"
        
        context = {
            'business_name': business_name,
            'urgency_level': urgency_level,
            'reason': reason,
            'conversation_id': conversation_id,
        }
        
        html_message = render_to_string('emails/urgent_alert.html', context)
        plain_message = render_to_string('emails/urgent_alert.txt', context)
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=self.from_email,
                recipient_list=[to_email],
                html_message=html_message,
                fail_silently=False
            )
            return True
        except Exception as e:
            logger.error(f"Error sending urgent alert: {e}")
            return False
    
    def send_missed_call_alert(
        self,
        to_email: str,
        business_name: str,
        phone_number: str,
        call_time: str
    ) -> bool:
        """Send missed call alert email."""
        subject = f"Missed Call Alert - {business_name}"
        
        context = {
            'business_name': business_name,
            'phone_number': phone_number,
            'call_time': call_time,
        }
        
        html_message = render_to_string('emails/missed_call.html', context)
        plain_message = render_to_string('emails/missed_call.txt', context)
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=self.from_email,
                recipient_list=[to_email],
                html_message=html_message,
                fail_silently=False
            )
            return True
        except Exception as e:
            logger.error(f"Error sending missed call alert: {e}")
            return False
    
    def send_new_lead_notification(
        self,
        to_email: str,
        business_name: str,
        contact_name: str,
        contact_phone: str,
        source: str
    ) -> bool:
        """Send new lead notification email."""
        subject = f"New Lead - {business_name}"
        
        context = {
            'business_name': business_name,
            'contact_name': contact_name,
            'contact_phone': contact_phone,
            'source': source,
        }
        
        html_message = render_to_string('emails/new_lead.html', context)
        plain_message = render_to_string('emails/new_lead.txt', context)
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=self.from_email,
                recipient_list=[to_email],
                html_message=html_message,
                fail_silently=False
            )
            return True
        except Exception as e:
            logger.error(f"Error sending new lead notification: {e}")
            return False
    
    def send_escalation_notification(
        self,
        to_email: str,
        business_name: str,
        conversation_id: str,
        reason: str
    ) -> bool:
        """Send escalation notification email."""
        subject = f"Conversation Escalated - {business_name}"
        
        context = {
            'business_name': business_name,
            'conversation_id': conversation_id,
            'reason': reason,
        }
        
        html_message = render_to_string('emails/escalation.html', context)
        plain_message = render_to_string('emails/escalation.txt', context)
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=self.from_email,
                recipient_list=[to_email],
                html_message=html_message,
                fail_silently=False
            )
            return True
        except Exception as e:
            logger.error(f"Error sending escalation notification: {e}")
            return False
