from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.accounts.api_urls')),
    path('dashboard/', include('apps.dashboard.api_urls')),
    path('calls/', include('apps.calls.api_urls')),
    path('messages/', include('apps.messages.api_urls')),
    path('contacts/', include('apps.contacts.api_urls')),
    path('conversations/', include('apps.conversations.api_urls')),
    path('knowledge/', include('apps.knowledge.api_urls')),
    path('notifications/', include('apps.notifications.api_urls')),
    path('analytics/', include('apps.analytics.api_urls')),
    path('integrations/', include('apps.integrations.api_urls')),
    path('business/', include('apps.businesses.api_urls')),
    path('receptionist/', include('apps.receptionist.api_urls')),
    path('demo/', include('apps.demo.api_urls')),
    path('webhooks/', include('apps.integrations.webhook_urls')),
]
