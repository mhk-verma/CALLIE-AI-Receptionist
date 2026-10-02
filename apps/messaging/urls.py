from django.urls import path
from . import views

app_name = 'messages'

urlpatterns = [
    path('', views.MessageListView.as_view(), name='list'),
    path('<uuid:pk>/', views.MessageDetailView.as_view(), name='detail'),
]
