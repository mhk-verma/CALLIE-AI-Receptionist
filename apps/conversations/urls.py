from django.urls import path
from . import views

app_name = 'conversations'

urlpatterns = [
    path('', views.ConversationListView.as_view(), name='list'),
    path('<uuid:pk>/', views.ConversationDetailView.as_view(), name='detail'),
]
