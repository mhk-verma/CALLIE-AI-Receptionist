from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from services.voice.twilio_service import get_voice_service
import logging

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class TwilioVoiceWebhookView(View):
    """Handle Twilio voice webhooks."""
    
    def post(self, request, *args, **kwargs):
        """Handle incoming call webhook."""
        try:
            voice_service = get_voice_service()
            
            # Get phone number from request
            from_number = request.POST.get('From', '')
            
            # Generate greeting TwiML
            from apps.businesses.models import Business
            # In production, match phone number to business
            # For now, use a default or demo business
            
            greeting = "Hello! Thank you for calling. My name is Callie, your virtual receptionist. How can I help you today?"
            
            twiml = voice_service.generate_twiml(greeting)
            
            return HttpResponse(twiml, content_type='application/xml')
        except Exception as e:
            logger.error(f"Error in Twilio voice webhook: {e}")
            return HttpResponse("Error", status=500)


@method_decorator(csrf_exempt, name='dispatch')
class TwilioStatusWebhookView(View):
    """Handle Twilio status callbacks."""
    
    def post(self, request, *args, **kwargs):
        """Handle call status updates."""
        try:
            call_sid = request.POST.get('CallSid')
            call_status = request.POST.get('CallStatus')
            
            # Update call record in database
            # This would update the Call model with the status
            
            logger.info(f"Call {call_sid} status: {call_status}")
            
            return HttpResponse("OK")
        except Exception as e:
            logger.error(f"Error in Twilio status webhook: {e}")
            return HttpResponse("Error", status=500)


@method_decorator(csrf_exempt, name='dispatch')
class MessageWebhookView(View):
    """Handle message webhooks from various platforms."""
    
    def post(self, request, *args, **kwargs):
        """Handle incoming message webhook."""
        try:
            # Parse webhook data based on platform
            platform = request.GET.get('platform', 'generic')
            
            if platform == 'whatsapp':
                # Handle WhatsApp webhook
                pass
            elif platform == 'instagram':
                # Handle Instagram webhook
                pass
            else:
                # Handle generic message webhook
                pass
            
            return HttpResponse("OK")
        except Exception as e:
            logger.error(f"Error in message webhook: {e}")
            return HttpResponse("Error", status=500)
