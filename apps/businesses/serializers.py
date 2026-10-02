from rest_framework import serializers
from .models import Business, BusinessHours, ReceptionistConfig, EscalationConfig


class BusinessHoursSerializer(serializers.ModelSerializer):
    """Serializer for BusinessHours model."""

    class Meta:
        model = BusinessHours
        fields = ['id', 'day', 'is_open', 'open_time', 'close_time']


class ReceptionistConfigSerializer(serializers.ModelSerializer):
    """Serializer for ReceptionistConfig model."""

    class Meta:
        model = ReceptionistConfig
        fields = [
            'id', 'name', 'personality', 'greeting', 'language', 'tone',
            'business_description', 'main_responsibilities',
            'max_conversation_length', 'escalation_threshold',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class EscalationConfigSerializer(serializers.ModelSerializer):
    """Serializer for EscalationConfig model."""

    class Meta:
        model = EscalationConfig
        fields = [
            'id', 'emergency_contact', 'owner_email', 'notification_preferences',
            'urgent_keywords', 'escalation_rules', 'auto_escalate_on_emergency',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class BusinessSerializer(serializers.ModelSerializer):
    """Serializer for Business model."""
    
    business_hours = BusinessHoursSerializer(many=True, read_only=True)
    receptionist_config = ReceptionistConfigSerializer(read_only=True)
    escalation_config = EscalationConfigSerializer(read_only=True)

    class Meta:
        model = Business
        fields = [
            'id', 'owner', 'name', 'business_type', 'phone', 'email',
            'address', 'website', 'description', 'logo', 'is_active',
            'business_hours', 'receptionist_config', 'escalation_config',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
