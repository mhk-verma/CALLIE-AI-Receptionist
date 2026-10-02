from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from apps.calls.models import Call
from apps.messages.models import Message
from apps.contacts.models import Contact
from apps.conversations.models import Conversation, UrgentFlag
from apps.businesses.models import Business


class DashboardAPIView(generics.GenericAPIView):
    """API endpoint for dashboard statistics."""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        
        try:
            business = Business.objects.get(owner=user)
        except Business.DoesNotExist:
            return Response({
                'error': 'No business found for this user'
            }, status=status.HTTP_404_NOT_FOUND)
        
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        stats = {
            'calls_today': Call.objects.filter(
                business=business,
                created_at__gte=today_start
            ).count(),
            'messages_today': Message.objects.filter(
                business=business,
                created_at__gte=today_start
            ).count(),
            'missed_calls': Call.objects.filter(
                business=business,
                status='missed',
                created_at__gte=today_start
            ).count(),
            'urgent_issues': UrgentFlag.objects.filter(
                conversation__business=business,
                created_at__gte=today_start
            ).count(),
            'new_contacts': Contact.objects.filter(
                business=business,
                created_at__gte=today_start
            ).count(),
            'ai_resolved': Conversation.objects.filter(
                business=business,
                resolution='ai_resolved',
                created_at__gte=today_start
            ).count(),
            'escalated': Conversation.objects.filter(
                business=business,
                resolution='escalated',
                created_at__gte=today_start
            ).count(),
            'customer_satisfaction': 98,  # Placeholder
        }
        
        # Recent activity
        recent_activity = []
        
        recent_calls = Call.objects.filter(business=business).order_by('-created_at')[:5]
        for call in recent_calls:
            recent_activity.append({
                'type': 'call',
                'title': 'Incoming Call',
                'subtitle': call.phone_number,
                'description': call.summary or 'No summary available',
                'time': call.created_at.isoformat(),
                'status': call.status,
            })
        
        recent_messages = Message.objects.filter(business=business).order_by('-created_at')[:5]
        for message in recent_messages:
            recent_activity.append({
                'type': 'message',
                'title': f'{message.channel.title()} Message',
                'subtitle': message.sender_name or 'Unknown',
                'description': message.content[:50] + '...' if len(message.content) > 50 else message.content,
                'time': message.created_at.isoformat(),
                'status': message.status,
            })
        
        recent_urgent = UrgentFlag.objects.filter(
            conversation__business=business
        ).order_by('-created_at')[:5]
        for urgent in recent_urgent:
            recent_activity.append({
                'type': 'urgent',
                'title': 'Urgent Flag',
                'subtitle': urgent.conversation.contact.name if urgent.conversation.contact else 'Unknown',
                'description': urgent.reason,
                'time': urgent.created_at.isoformat(),
                'status': 'urgent',
            })
        
        # Sort by time
        recent_activity.sort(key=lambda x: x['time'], reverse=True)
        recent_activity = recent_activity[:10]
        
        return Response({
            'stats': stats,
            'recent_activity': recent_activity,
            'business': {
                'id': str(business.id),
                'name': business.name,
            }
        })
