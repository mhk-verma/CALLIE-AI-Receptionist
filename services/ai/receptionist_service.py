"""
AI Receptionist service for handling customer interactions.
"""
from typing import Dict, List, Optional
from apps.businesses.models import Business, ReceptionistConfig, EscalationConfig
from apps.knowledge.models import FAQ, KnowledgeBaseEntry
from .llm_service import get_llm_provider


class ReceptionistService:
    """Service for AI receptionist operations."""
    
    def __init__(self, business: Business):
        self.business = business
        self.config = business.receptionist_config
        self.escalation_config = business.escalation_config
        self.llm = get_llm_provider()
    
    def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Generate a response to a user message.
        
        Returns:
            Dict with keys: response, intent, urgency, should_escalate
        """
        # Get system prompt
        system_prompt = self._build_system_prompt()
        
        # Build conversation context
        full_prompt = self._build_prompt(user_message, conversation_history, context)
        
        # Generate response
        response = self.llm.generate_response(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=500
        )
        
        # Classify intent
        intent = self._classify_intent(user_message)
        
        # Detect urgency
        urgency = self._detect_urgency(user_message)
        
        # Determine if escalation is needed
        should_escalate = self._should_escalate(user_message, urgency, conversation_history)
        
        return {
            'response': response,
            'intent': intent,
            'urgency': urgency,
            'should_escalate': should_escalate
        }
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the AI."""
        system_prompt = f"""You are {self.config.name}, a virtual receptionist for {self.business.name}.

Personality: {self.config.personality}
Tone: {self.config.tone}

Business Description:
{self.config.business_description or self.business.description}

Main Responsibilities:
{self.config.main_responsibilities or 'Answer questions, provide information, and assist customers.'}

Important Rules:
1. Only answer using the information provided about the business.
2. If you don't know the answer, say you don't have that information and offer to connect them with a staff member.
3. Be concise and professional.
4. Do not make promises you cannot keep.
5. Detect urgent situations and escalate when necessary.
6. Be friendly but professional.
7. If the customer seems frustrated or angry, be empathetic and offer to connect them with a human.
"""
        return system_prompt
    
    def _build_prompt(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None,
        context: Optional[Dict] = None
    ) -> str:
        """Build the full prompt with context."""
        prompt = user_message
        
        # Add conversation history
        if conversation_history:
            history_text = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in conversation_history[-5:]  # Last 5 messages
            ])
            prompt = f"Previous conversation:\n{history_text}\n\nCurrent message: {user_message}"
        
        # Add relevant FAQs
        relevant_faqs = self._get_relevant_faqs(user_message)
        if relevant_faqs:
            faq_text = "\n".join([
                f"Q: {faq.question}\nA: {faq.answer}"
                for faq in relevant_faqs
            ])
            prompt = f"Frequently Asked Questions:\n{faq_text}\n\n{prompt}"
        
        # Add business hours
        if context and context.get('check_hours'):
            hours = self._get_business_hours_text()
            prompt = f"Business Hours:\n{hours}\n\n{prompt}"
        
        return prompt
    
    def _get_relevant_faqs(self, message: str) -> List[FAQ]:
        """Get relevant FAQs based on the message."""
        # Simple keyword matching for now
        # In production, use semantic search with embeddings
        message_lower = message.lower()
        
        all_faqs = FAQ.objects.filter(
            business=self.business,
            is_active=True
        )
        
        relevant = []
        for faq in all_faqs:
            # Check if any word in FAQ matches message
            faq_words = set(faq.question.lower().split())
            message_words = set(message_lower.split())
            
            if faq_words & message_words:  # Intersection
                relevant.append(faq)
        
        # Sort by priority and return top 3
        relevant.sort(key=lambda x: x.priority, reverse=True)
        return relevant[:3]
    
    def _get_business_hours_text(self) -> str:
        """Get business hours as text."""
        hours = self.business.business_hours.filter(is_open=True)
        hours_text = "\n".join([
            f"{h.get_day_display()}: {h.open_time} - {h.close_time}"
            for h in hours
        ])
        return hours_text
    
    def _classify_intent(self, message: str) -> str:
        """Classify the intent of the message."""
        intents = [
            'general_inquiry',
            'appointment',
            'pricing',
            'hours',
            'location',
            'services',
            'support',
            'complaint',
            'emergency'
        ]
        
        scores = self.llm.classify_intent(message, intents)
        
        # Return the intent with highest score
        return max(scores, key=scores.get)
    
    def _detect_urgency(self, message: str) -> str:
        """Detect the urgency level of the message."""
        scores = self.llm.detect_urgency(message)
        
        # Return the urgency with highest score
        return max(scores, key=scores.get)
    
    def _should_escalate(
        self,
        message: str,
        urgency: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> bool:
        """Determine if the conversation should be escalated."""
        # Auto-escalate on emergency
        if urgency == 'emergency' and self.escalation_config.auto_escalate_on_emergency:
            return True
        
        # Check for urgent keywords
        urgent_keywords = self.escalation_config.get_urgent_keywords_list()
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in urgent_keywords):
            return True
        
        # Check conversation length
        if conversation_history and len(conversation_history) >= self.config.escalation_threshold:
            return True
        
        return False
    
    def get_greeting(self) -> str:
        """Get the receptionist's greeting."""
        return self.config.get_formatted_greeting()
