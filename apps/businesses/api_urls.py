from django.urls import path
from . import api_views

app_name = 'businesses'

urlpatterns = [
    path('', api_views.BusinessListAPIView.as_view(), name='api_list'),
    path('<uuid:pk>/', api_views.BusinessDetailAPIView.as_view(), name='api_detail'),
    path('<uuid:pk>/hours/', api_views.BusinessHoursAPIView.as_view(), name='api_hours'),
    path('<uuid:pk>/receptionist/', api_views.ReceptionistConfigAPIView.as_view(), name='api_receptionist'),
    path('<uuid:pk>/escalation/', api_views.EscalationConfigAPIView.as_view(), name='api_escalation'),
]
