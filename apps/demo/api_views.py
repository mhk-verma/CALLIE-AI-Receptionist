from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.businesses.models import Business
from apps.contacts.models import Contact
from apps.conversations.models import Conversation, ConversationMessage, UrgentFlag
from apps.calls.models import Call
from apps.messages.models import Message
from services.ai.receptionist_service import ReceptionistService
from django.utils import timezone


class SimulateCallAPIView(generics.GenericAPIView):
    """API endpoint for simulating a call."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        business = Business.objects.get(owner=request.user)
        receptionist_service = ReceptionistService(business)
        
        user_message = request.data.get('message', '')
        conversation_id = request.data.get('conversation_id')
        is_urgent = request.data.get('is_urgent', False)
        
        # Get or create conversation
        if conversation_id:
            conversation = Conversation.objects.get(id=conversation_id)
        else:
            contact = Contact.objects.create(
                business=business,
                name="Demo Customer",
                phone="+15555555555",
                source='call'
            )
            
            conversation = Conversation.objects.create(
                business=business,
                contact=contact,
                channel=Conversation.Channel.CALL
            )
            
            call = Call.objects.create(
                business=business,
                contact=contact,
                phone_number="+15555555555",
                caller_name="Demo Customer",
                status=Call.Status.ANSWERED,
                handled_by='ai'
            )
        
        # Get conversation history
        history = ConversationMessage.objects.filter(
            conversation=conversation
        ).order_by('timestamp')
        
        history_list = [
            {'role': msg.sender, 'content': msg.content}
            for msg in history
        ]
        
        # Generate AI response
        if is_urgent:
            response = "I understand this is urgent. Let me escalate this to a staff member immediately who can help you right away."
            urgency = 'urgent'
            should_escalate = True
            intent = 'emergency'
        else:
            result = receptionist_service.generate_response(
                user_message,
                history_list
            )
            response = result['response']
            urgency = result['urgency']
            should_escalate = result['should_escalate']
            intent = result['intent']
        
        # Save messages
        ConversationMessage.objects.create(
            conversation=conversation,
            sender='customer',
            content=user_message
        )
        
        ConversationMessage.objects.create(
            conversation=conversation,
            sender='ai',
            content=response
        )
        
        # Update conversation
        conversation.summary = f"Customer: {user_message[:100]}..."
        conversation.customer_intent = intent
        conversation.ended_at = timezone.now()
        
        if should_escalate:
            conversation.resolution = Conversation.Resolution.ESCALATED
            UrgentFlag.objects.create(
                conversation=conversation,
                level=urgency.upper(),
                reason=f"Demo urgent call: {user_message}"
            )
        else:
            conversation.resolution = Conversation.Resolution.AI_RESOLVED
        
        conversation.save()
        
        return Response({
            'response': response,
            'conversation_id': str(conversation.id),
            'urgency': urgency,
            'should_escalate': should_escalate,
            'intent': intent
        })


class SimulateMessageAPIView(generics.GenericAPIView):
    """API endpoint for simulating a message."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        business = Business.objects.get(owner=request.user)
        receptionist_service = ReceptionistService(business)
        
        user_message = request.data.get('message', '')
        channel = request.data.get('channel', 'sms')
        sender_name = request.data.get('sender_name', 'Demo Customer')
        
        contact = Contact.objects.create(
            business=business,
            name=sender_name,
            phone="+15555555555",
            source='message'
        )
        
        conversation = Conversation.objects.create(
            business=business,
            contact=contact,
            channel=channel
        )
        
        result = receptionist_service.generate_response(user_message)
        response = result['response']
        
        message = Message.objects.create(
            business=business,
            contact=contact,
            conversation=conversation,
            sender_name=sender_name,
            sender_number="+15555555555",
            channel=channel,
            content=user_message,
            ai_response=response,
            status=Message.Status.SENT,
            direction='inbound'
        )
        
        conversation.summary = f"Message: {user_message[:100]}..."
        conversation.customer_intent = result['intent']
        conversation.resolution = Conversation.Resolution.AI_RESOLVED
        conversation.ended_at = timezone.now()
        conversation.save()
        
        return Response({
            'response': response,
            'message_id': str(message.id),
            'conversation_id': str(conversation.id)
        })
