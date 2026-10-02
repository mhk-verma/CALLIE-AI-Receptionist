from django.urls import path
from . import views

app_name = 'demo'

urlpatterns = [
    path('', views.DemoHomeView.as_view(), name='home'),
    path('simulate-call/', views.SimulateCallView.as_view(), name='simulate_call'),
]
