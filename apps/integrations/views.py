from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Integration


@method_decorator(login_required, name='dispatch')
class IntegrationListView(ListView):
    """List all integrations."""
    model = Integration
    template_name = 'integrations/list.html'
    context_object_name = 'integrations'

    def get_queryset(self):
        from apps.businesses.models import Business
        try:
            business = Business.objects.get(owner=self.request.user)
            return Integration.objects.filter(business=business)
        except Business.DoesNotExist:
            return Integration.objects.none()
