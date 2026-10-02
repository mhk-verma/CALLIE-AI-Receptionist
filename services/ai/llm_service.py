"""
Base LLM service interface and implementations.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from django.conf import settings


class BaseLLMProvider(ABC):
    """Base class for LLM providers."""
    
    def __init__(self):
        self.provider_name = "base"
    
    @abstractmethod
    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs
    ) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    def classify_intent(self, text: str, intents: List[str]) -> Dict[str, float]:
        """Classify the intent of the given text."""
        pass
    
    @abstractmethod
    def detect_urgency(self, text: str) -> Dict[str, float]:
        """Detect urgency level in the text."""
        pass
    
    @abstractmethod
    def summarize_conversation(self, messages: List[Dict]) -> str:
        """Summarize a conversation."""
        pass


class GroqProvider(BaseLLMProvider):
    """Groq LLM provider implementation (FREE - uses OpenAI-compatible API)."""
    
    def __init__(self):
        super().__init__()
        self.provider_name = "groq"
        self.api_key = getattr(settings, 'GROQ_API_KEY', '')
        self.model = "qwen-2.5-72b-instruct"  # Free, current model
        self.base_url = "https://api.groq.com/openai/v1"
        
        if not self.api_key:
            raise ValueError("Groq API key not configured")
    
    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs
    ) -> str:
        """Generate response using Groq API (FREE)."""
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq API error: {e}")
            return "I apologize, but I'm having trouble processing your request right now."
    
    def classify_intent(self, text: str, intents: List[str]) -> Dict[str, float]:
        """Classify intent using Groq."""
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            
            prompt = f"Classify the following text into one of these intents: {', '.join(intents)}\n\nText: {text}\n\nRespond with just the intent name."
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=50
            )
            
            intent = response.choices[0].message.content.strip().lower()
            
            # Return scores
            scores = {intent.lower(): 0.9}
            for i in intents:
                if i.lower() not in scores:
                    scores[i.lower()] = 0.1
            
            return scores
        except Exception as e:
            print(f"Intent classification error: {e}")
            return {intent.lower(): 0.5 for intent in intents}
    
    def detect_urgency(self, text: str) -> Dict[str, float]:
        """Detect urgency using Groq."""
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            
            prompt = f"Classify the urgency level of this text as one of: normal, important, urgent, emergency\n\nText: {text}\n\nRespond with just the urgency level."
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=20
            )
            
            urgency = response.choices[0].message.content.strip().lower()
            
            levels = ['normal', 'important', 'urgent', 'emergency']
            scores = {level: 0.1 for level in levels}
            scores[urgency] = 0.9
            
            return scores
        except Exception as e:
            print(f"Urgency detection error: {e}")
            return {'normal': 0.8, 'important': 0.1, 'urgent': 0.05, 'emergency': 0.05}
    
    def summarize_conversation(self, messages: List[Dict]) -> str:
        """Summarize conversation using Groq."""
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            
            conversation_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
            prompt = f"Summarize this conversation in 2-3 sentences:\n\n{conversation_text}"
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=150
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Summarization error: {e}")
            return "Conversation summary unavailable."


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider implementation."""
    
    def __init__(self):
        super().__init__()
        self.provider_name = "openai"
        self.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-3.5-turbo"
        self.base_url = "https://api.openai.com/v1"
        
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
    
    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs
    ) -> str:
        """Generate response using OpenAI API."""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "I apologize, but I'm having trouble processing your request right now."
    
    def classify_intent(self, text: str, intents: List[str]) -> Dict[str, float]:
        """Classify intent using OpenAI."""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            prompt = f"Classify the following text into one of these intents: {', '.join(intents)}\n\nText: {text}\n\nRespond with just the intent name."
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=50
            )
            
            intent = response.choices[0].message.content.strip().lower()
            
            # Return scores
            scores = {intent.lower(): 0.9}
            for i in intents:
                if i.lower() not in scores:
                    scores[i.lower()] = 0.1
            
            return scores
        except Exception as e:
            print(f"Intent classification error: {e}")
            return {intent.lower(): 0.5 for intent in intents}
    
    def detect_urgency(self, text: str) -> Dict[str, float]:
        """Detect urgency using OpenAI."""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            prompt = f"Classify the urgency level of this text as one of: normal, important, urgent, emergency\n\nText: {text}\n\nRespond with just the urgency level."
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=20
            )
            
            urgency = response.choices[0].message.content.strip().lower()
            
            levels = ['normal', 'important', 'urgent', 'emergency']
            scores = {level: 0.1 for level in levels}
            scores[urgency] = 0.9
            
            return scores
        except Exception as e:
            print(f"Urgency detection error: {e}")
            return {'normal': 0.8, 'important': 0.1, 'urgent': 0.05, 'emergency': 0.05}
    
    def summarize_conversation(self, messages: List[Dict]) -> str:
        """Summarize conversation using OpenAI."""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            conversation_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
            prompt = f"Summarize this conversation in 2-3 sentences:\n\n{conversation_text}"
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=150
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Summarization error: {e}")
            return "Conversation summary unavailable."


class DemoAIProvider(BaseLLMProvider):
    """Demo AI provider for testing without API keys - Enhanced for realistic responses."""
    
    def __init__(self):
        super().__init__()
        self.provider_name = "demo"
    
    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs
    ) -> str:
        """Generate a demo response with enhanced intelligence."""
        prompt_lower = prompt.lower()
        
        # Enhanced pattern matching for demo
        if any(word in prompt_lower for word in ['hour', 'open', 'close', 'time', 'when']):
            return "We're open Monday through Friday from 9 AM to 6 PM, and on Saturdays from 10 AM to 2 PM. We're closed on Sundays. Would you like to schedule an appointment during our business hours?"
        elif any(word in prompt_lower for word in ['appointment', 'book', 'schedule', 'reserve']):
            return "I'd be happy to help you schedule an appointment! I can check our availability for you. What date and time would work best for you? Also, which service would you like to book?"
        elif any(word in prompt_lower for word in ['price', 'cost', 'how much', 'charge', 'fee']):
            return "Our pricing varies depending on the service you need. For general consultations, we charge $50. For specialized services, pricing starts at $100. Would you like me to provide detailed pricing for a specific service?"
        elif any(word in prompt_lower for word in ['location', 'address', 'where', 'direction']):
            return "We're located at 123 Main Street, downtown. We have free parking available in the rear of the building. The nearest subway station is just 2 blocks away. Would you like me to send you directions?"
        elif any(word in prompt_lower for word in ['payment', 'pay', 'card', 'cash', 'credit']):
            return "We accept all major credit cards (Visa, MasterCard, American Express), debit cards, and cash payments. We also offer payment plans for larger services. We do not accept personal checks at this time."
        elif any(word in prompt_lower for word in ['emergency', 'urgent', 'immediately', 'critical', 'help']):
            return "I understand this is urgent. I'm connecting you with our emergency line right now. Please stay on the line while I transfer you to a staff member who can assist you immediately."
        elif any(word in prompt_lower for word in ['service', 'offer', 'provide', 'do you do']):
            return "We offer a wide range of services including consultations, specialized treatments, and emergency care. Our team of experts is here to help with various needs. Would you like me to explain any specific service in detail?"
        elif any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return "Hello! Thank you for calling. My name is Callie, your virtual receptionist. I'm here to help you with appointments, questions about our services, pricing information, or any other assistance you need. How can I help you today?"
        elif any(word in prompt_lower for word in ['thank', 'thanks', 'appreciate']):
            return "You're very welcome! Is there anything else I can help you with today? I'm happy to assist with any other questions or schedule an appointment for you."
        elif any(word in prompt_lower for word in ['bye', 'goodbye', 'see you']):
            return "Thank you for calling! Have a wonderful day, and we look forward to serving you again soon. Goodbye!"
        elif any(word in prompt_lower for word in ['speak', 'human', 'person', 'representative']):
            return "I understand you'd like to speak with a human. I can transfer you to one of our staff members. May I ask what this is regarding so I can connect you with the right person?"
        else:
            return "Thank you for your question. While I'm a virtual assistant, I want to make sure you get the most accurate information. Would you like me to take a message and have a staff member get back to you, or is there something specific about our services, hours, or pricing I can help with?"
    
    def classify_intent(self, text: str, intents: List[str]) -> Dict[str, float]:
        """Classify intent using simple keyword matching."""
        text_lower = text.lower()
        scores = {intent.lower(): 0.1 for intent in intents}
        
        # Simple keyword matching
        if 'hour' in text_lower or 'open' in text_lower or 'time' in text_lower:
            if 'hours' in intents:
                scores['hours'] = 0.9
        elif 'appointment' in text_lower or 'book' in text_lower:
            if 'appointment' in intents:
                scores['appointment'] = 0.9
        elif 'price' in text_lower or 'cost' in text_lower:
            if 'pricing' in intents:
                scores['pricing'] = 0.9
        elif 'location' in text_lower or 'address' in text_lower:
            if 'location' in intents:
                scores['location'] = 0.9
        
        return scores
    
    def detect_urgency(self, text: str) -> Dict[str, float]:
        """Detect urgency using keyword matching."""
        text_lower = text.lower()
        scores = {'normal': 0.8, 'important': 0.1, 'urgent': 0.05, 'emergency': 0.05}
        
        urgent_keywords = ['emergency', 'urgent', 'immediately', 'critical', 'accident', 'cannot wait']
        important_keywords = ['important', 'asap', 'soon', 'priority']
        
        if any(keyword in text_lower for keyword in urgent_keywords):
            scores = {'normal': 0.1, 'important': 0.1, 'urgent': 0.3, 'emergency': 0.5}
        elif any(keyword in text_lower for keyword in important_keywords):
            scores = {'normal': 0.3, 'important': 0.5, 'urgent': 0.1, 'emergency': 0.1}
        
        return scores
    
    def summarize_conversation(self, messages: List[Dict]) -> str:
        """Summarize conversation using simple extraction."""
        if not messages:
            return "No conversation to summarize."
        
        # Get the last user message
        user_messages = [m for m in messages if m.get('role') == 'user']
        if user_messages:
            last_message = user_messages[-1]['content']
            return f"Customer asked about: {last_message[:100]}..."
        
        return "Conversation summary unavailable."


def get_llm_provider() -> BaseLLMProvider:
    """Factory function to get the appropriate LLM provider."""
    if settings.DEMO_MODE:
        return DemoAIProvider()
    
    provider = settings.AI_PROVIDER.lower()
    
    if provider == 'groq':
        try:
            return GroqProvider()
        except ValueError:
            print("Groq API key not configured, falling back to demo mode")
            return DemoAIProvider()
    elif provider == 'openai':
        try:
            return OpenAIProvider()
        except ValueError:
            print("OpenAI API key not configured, falling back to demo mode")
            return DemoAIProvider()
    else:
        return DemoAIProvider()
