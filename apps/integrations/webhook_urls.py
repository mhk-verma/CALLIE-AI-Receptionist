from django.urls import path
from . import webhook_views

app_name = 'webhooks'

urlpatterns = [
    path('twilio/voice/', webhook_views.TwilioVoiceWebhookView.as_view(), name='twilio_voice'),
    path('twilio/status/', webhook_views.TwilioStatusWebhookView.as_view(), name='twilio_status'),
    path('messages/', webhook_views.MessageWebhookView.as_view(), name='messages'),
]
