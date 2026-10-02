from django.urls import path
from . import views

app_name = 'calls'

urlpatterns = [
    path('', views.CallListView.as_view(), name='list'),
    path('<uuid:pk>/', views.CallDetailView.as_view(), name='detail'),
]
