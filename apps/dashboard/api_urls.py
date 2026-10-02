from django.urls import path
from . import api_views

app_name = 'dashboard'

urlpatterns = [
    path('', api_views.DashboardAPIView.as_view(), name='api_dashboard'),
]
