from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import Call


@method_decorator(login_required, name='dispatch')
class CallListView(ListView):
    """List all calls."""
    model = Call
    template_name = 'calls/list.html'
    context_object_name = 'calls'
    paginate_by = 20

    def get_queryset(self):
        from apps.businesses.models import Business
        try:
            business = Business.objects.get(owner=self.request.user)
            return Call.objects.filter(business=business)
        except Business.DoesNotExist:
            return Call.objects.none()


@method_decorator(login_required, name='dispatch')
class CallDetailView(DetailView):
    """View call details."""
    model = Call
    template_name = 'calls/detail.html'
    context_object_name = 'call'
