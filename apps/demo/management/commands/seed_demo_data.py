from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.businesses.models import Business, BusinessHours, ReceptionistConfig, EscalationConfig
from apps.contacts.models import Contact
from apps.calls.models import Call
from apps.messages.models import Message
from apps.conversations.models import Conversation, ConversationMessage, UrgentFlag
from apps.knowledge.models import FAQ, KnowledgeBaseEntry
from django.utils import timezone
from datetime import timedelta
import uuid

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed demo data for the AI Receptionist application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding demo data...')

        # Create demo user
        demo_user, created = User.objects.get_or_create(
            email='demo@example.com',
            defaults={
                'first_name': 'Demo',
                'last_name': 'User',
                'role': User.Role.OWNER,
                'is_active': True,
                'email_verified': True,
                'onboarding_completed': True,
            }
        )
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS('Created demo user: demo@example.com / demo123'))
        else:
            self.stdout.write('Demo user already exists')

        # Create demo business
        demo_business, created = Business.objects.get_or_create(
            owner=demo_user,
            defaults={
                'name': 'Callie Demo Services',
                'business_type': 'Professional Services',
                'phone': '+1 (555) 123-4567',
                'email': 'info@calliedemo.com',
                'address': '123 Demo Street, Demo City, DC 12345',
                'website': 'https://calliedemo.com',
                'description': 'A demo business showcasing the AI Receptionist capabilities.',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created demo business'))

            # Create business hours
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
                BusinessHours.objects.create(
                    business=demo_business,
                    day=day,
                    is_open=True,
                    open_time='09:00',
                    close_time='18:00'
                )
            
            # Weekend hours
            for day in ['saturday', 'sunday']:
                BusinessHours.objects.create(
                    business=demo_business,
                    day=day,
                    is_open=True,
                    open_time='10:00',
                    close_time='14:00'
                )

            # Create receptionist config
            ReceptionistConfig.objects.create(
                business=demo_business,
                name='Callie',
                personality='Friendly, professional and concise.',
                greeting='Hello! Thank you for calling Callie Demo Services. My name is Callie, your virtual receptionist. How can I help you today?',
                language='en',
                tone='professional',
                business_description='Callie Demo Services provides professional consulting and support services.',
                main_responsibilities='Answer calls, handle inquiries, schedule appointments, and escalate urgent matters.',
            )

            # Create escalation config
            EscalationConfig.objects.create(
                business=demo_business,
                emergency_contact='+1 (555) 999-8888',
                owner_email='demo@example.com',
                urgent_keywords='emergency,urgent,immediately,critical,accident,cannot wait',
                auto_escalate_on_emergency=True,
            )

            # Create FAQs
            faqs = [
                {
                    'question': 'What are your business hours?',
                    'answer': 'We are open Monday to Friday from 9 AM to 6 PM, and weekends from 10 AM to 2 PM.',
                    'category': 'hours',
                    'priority': 10,
                },
                {
                    'question': 'How can I schedule an appointment?',
                    'answer': 'You can schedule an appointment by calling us during business hours or through our website.',
                    'category': 'appointment',
                    'priority': 9,
                },
                {
                    'question': 'What services do you offer?',
                    'answer': 'We offer professional consulting, technical support, and project management services.',
                    'category': 'services',
                    'priority': 8,
                },
                {
                    'question': 'What are your payment options?',
                    'answer': 'We accept all major credit cards, bank transfers, and PayPal.',
                    'category': 'payment',
                    'priority': 7,
                },
            ]
            
            for faq_data in faqs:
                FAQ.objects.create(business=demo_business, **faq_data)

            # Create knowledge base entries
            kb_entries = [
                {
                    'title': 'About Our Company',
                    'content': 'Callie Demo Services has been providing exceptional service since 2020. We specialize in helping businesses improve their customer communications.',
                    'category': 'business_info',
                    'priority': 10,
                },
                {
                    'title': 'Pricing Information',
                    'content': 'Our pricing is competitive and tailored to each client\'s needs. Contact us for a custom quote.',
                    'category': 'pricing',
                    'priority': 9,
                },
            ]
            
            for kb_data in kb_entries:
                KnowledgeBaseEntry.objects.create(business=demo_business, **kb_data)

            # Create demo contacts
            contacts = [
                {
                    'name': 'John Smith',
                    'phone': '+1 (555) 111-2222',
                    'email': 'john@example.com',
                    'company': 'ABC Corp',
                    'tags': ['VIP', 'Regular'],
                    'source': 'call',
                },
                {
                    'name': 'Jane Doe',
                    'phone': '+1 (555) 333-4444',
                    'email': 'jane@example.com',
                    'company': 'XYZ Inc',
                    'tags': ['New Lead'],
                    'source': 'message',
                },
            ]
            
            for contact_data in contacts:
                Contact.objects.create(business=demo_business, **contact_data)

            # Create demo calls
            for i in range(5):
                contact = demo_business.contacts.first()
                call = Call.objects.create(
                    business=demo_business,
                    contact=contact,
                    phone_number='+1 (555) 555-5555',
                    caller_name='Demo Caller',
                    status=Call.Status.ANSWERED,
                    urgency=Call.Urgency.NORMAL,
                    duration=120 + (i * 30),
                    handled_by='ai',
                    summary='Customer asked about business hours.',
                    customer_intent='hours',
                    resolution='ai_resolved',
                )
                
                # Create transcript
                ConversationMessage.objects.create(
                    sender='customer',
                    content='What are your hours today?',
                    timestamp=timezone.now() - timedelta(hours=i)
                )
                
                ConversationMessage.objects.create(
                    sender='ai',
                    content='We are open from 9 AM to 6 PM today.',
                    timestamp=timezone.now() - timedelta(hours=i)
                )

            # Create demo messages
            channels = ['sms', 'whatsapp', 'instagram']
            for i, channel in enumerate(channels):
                contact = demo_business.contacts.all()[i % 2]
                Message.objects.create(
                    business=demo_business,
                    contact=contact,
                    sender_name='Demo Customer',
                    sender_number='+1 (555) 666-7777',
                    channel=channel,
                    content='Do you have availability tomorrow?',
                    ai_response='Yes, we have availability tomorrow. What time works best for you?',
                    status='sent',
                    direction='inbound',
                )

            # Create urgent flag demo
            urgent_conversation = Conversation.objects.create(
                business=demo_business,
                contact=demo_business.contacts.first(),
                channel=Conversation.Channel.CALL,
                summary='Customer reported an emergency situation.',
                customer_intent='emergency',
                resolution='escalated',
            )
            
            UrgentFlag.objects.create(
                conversation=urgent_conversation,
                level='URGENT',
                reason='Customer mentioned emergency situation requiring immediate attention.',
                keywords_detected=['emergency'],
            )

            self.stdout.write(self.style.SUCCESS('Demo data seeded successfully!'))
            self.stdout.write('Login credentials: demo@example.com / demo123')
        else:
            self.stdout.write('Demo business already exists')
