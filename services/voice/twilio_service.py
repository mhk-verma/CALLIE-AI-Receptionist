"""
Twilio voice service for handling phone calls.
"""
from typing import Dict, Optional
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class TwilioVoiceService:
    """Service for Twilio voice integration."""
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.phone_number = settings.TWILIO_PHONE_NUMBER
        
        if not all([self.account_sid, self.auth_token, self.phone_number]):
            logger.warning("Twilio credentials not configured")
    
    def generate_twiml(self, text: str, voice: str = 'alice') -> str:
        """Generate TwiML for text-to-speech."""
        twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" action="/api/webhooks/twilio/speech/" method="POST" timeout="5" speechTimeout="auto">
        <Say voice="{voice}">{text}</Say>
    </Gather>
</Response>'''
        return twiml
    
    def generate_gather_twiml(self, text: str, action_url: str, voice: str = 'alice') -> str:
        """Generate TwiML for gathering speech input."""
        twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" action="{action_url}" method="POST" timeout="5" speechTimeout="auto">
        <Say voice="{voice}">{text}</Say>
    </Gather>
    <Say voice="{voice}">I didn't hear you. Goodbye.</Say>
</Response>'''
        return twiml
    
    def generate_hangup_twiml(self, text: str = "Thank you for calling. Goodbye!") -> str:
        """Generate TwiML for hanging up."""
        twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{text}</Say>
    <Hangup/>
</Response>'''
        return twiml
    
    def make_call(self, to_number: str, url: str) -> Optional[Dict]:
        """Make an outbound call using Twilio."""
        try:
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            
            call = client.calls.create(
                to=to_number,
                from_=self.phone_number,
                url=url,
                method='POST'
            )
            
            return {
                'call_sid': call.sid,
                'status': call.status,
                'direction': call.direction
            }
        except Exception as e:
            logger.error(f"Error making call: {e}")
            return None
    
    def get_recording(self, recording_sid: str) -> Optional[str]:
        """Get recording URL from Twilio."""
        try:
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            recording = client.recordings(recording_sid).fetch()
            
            return recording.uri
        except Exception as e:
            logger.error(f"Error getting recording: {e}")
            return None
    
    def is_configured(self) -> bool:
        """Check if Twilio is properly configured."""
        return bool(
            self.account_sid and 
            self.auth_token and 
            self.phone_number
        )


class DemoVoiceService:
    """Demo voice service for testing without Twilio."""
    
    def __init__(self):
        self.phone_number = "+15555555555"  # Demo number
    
    def generate_twiml(self, text: str, voice: str = 'alice') -> str:
        """Generate demo TwiML."""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="{voice}">{text}</Say>
</Response>'''
    
    def generate_gather_twiml(self, text: str, action_url: str, voice: str = 'alice') -> str:
        """Generate demo gather TwiML."""
        return self.generate_twiml(text, voice)
    
    def generate_hangup_twiml(self, text: str = "Thank you for calling. Goodbye!") -> str:
        """Generate demo hangup TwiML."""
        return self.generate_twiml(text)
    
    def make_call(self, to_number: str, url: str) -> Optional[Dict]:
        """Demo call - doesn't actually make a call."""
        return {
            'call_sid': 'demo_call_sid',
            'status': 'ringing',
            'direction': 'outbound-api'
        }
    
    def get_recording(self, recording_sid: str) -> Optional[str]:
        """Demo recording - returns None."""
        return None
    
    def is_configured(self) -> bool:
        """Demo service is always configured."""
        return True


def get_voice_service():
    """Factory function to get the appropriate voice service."""
    if settings.DEMO_MODE or not settings.TWILIO_ACCOUNT_SID:
        return DemoVoiceService()
    
    return TwilioVoiceService()
