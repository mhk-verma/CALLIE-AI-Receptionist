from django.urls import path
from . import api_views

app_name = 'demo'

urlpatterns = [
    path('simulate-call/', api_views.SimulateCallAPIView.as_view(), name='api_simulate_call'),
    path('simulate-message/', api_views.SimulateMessageAPIView.as_view(), name='api_simulate_message'),
]
