from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('business/', include('apps.businesses.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('demo/', include('apps.demo.urls')),
    path('api/webhooks/', include('apps.integrations.webhook_urls')),
    
    # Landing page
    path('', TemplateView.as_view(template_name='landing/index.html'), name='landing'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
