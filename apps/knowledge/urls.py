from django.urls import path
from . import views

app_name = 'knowledge'

urlpatterns = [
    path('faqs/', views.FAQListView.as_view(), name='faqs'),
    path('faqs/create/', views.FAQCreateView.as_view(), name='faq_create'),
    path('faqs/<uuid:pk>/edit/', views.FAQUpdateView.as_view(), name='faq_edit'),
    path('faqs/<uuid:pk>/delete/', views.FAQDeleteView.as_view(), name='faq_delete'),
    path('knowledge-base/', views.KnowledgeBaseListView.as_view(), name='knowledge_base'),
    path('knowledge-base/create/', views.KnowledgeBaseCreateView.as_view(), name='kb_create'),
]
