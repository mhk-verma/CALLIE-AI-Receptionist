from django.urls import path
from . import views

app_name = 'businesses'

urlpatterns = [
    path('create/', views.BusinessCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.BusinessDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.BusinessUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/hours/', views.BusinessHoursView.as_view(), name='hours'),
    path('<uuid:pk>/receptionist/', views.ReceptionistConfigView.as_view(), name='receptionist'),
    path('<uuid:pk>/escalation/', views.EscalationConfigView.as_view(), name='escalation'),
]
