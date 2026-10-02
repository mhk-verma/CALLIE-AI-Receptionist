"""
Test script to verify Groq AI integration is working.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from services.ai.llm_service import get_llm_provider

print("=" * 60)
print("Testing Groq AI Integration (FREE)")
print("=" * 60)

try:
    # Get the AI provider
    llm = get_llm_provider()
    print(f"\n[OK] AI Provider: {llm.provider_name}")
    print(f"[OK] Using real AI: {not llm.provider_name == 'demo'}")

    # Test response generation
    print("\n[TEST] Testing AI Response Generation...")
    test_question = "What are your business hours?"
    response = llm.generate_response(test_question)

    print(f"\n[Q] Question: {test_question}")
    print(f"[A] AI Response: {response}")

    # Test urgency detection
    print("\n[TEST] Testing Urgency Detection...")
    urgency = llm.detect_urgency("This is an emergency, I need help immediately!")
    print(f"Urgency scores: {urgency}")

    # Test intent classification
    print("\n[TEST] Testing Intent Classification...")
    intents = ['appointment', 'hours', 'pricing', 'emergency']
    intent_scores = llm.classify_intent("I need to book an appointment", intents)
    print(f"Intent scores: {intent_scores}")

    print("\n" + "=" * 60)
    print("[SUCCESS] AI Integration is WORKING!")
    print("=" * 60)

except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
