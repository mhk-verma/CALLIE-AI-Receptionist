from django.urls import path
from . import views

app_name = 'integrations'

urlpatterns = [
    path('', views.IntegrationListView.as_view(), name='list'),
]
