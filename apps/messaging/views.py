from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import Message


@method_decorator(login_required, name='dispatch')
class MessageListView(ListView):
    """List all messages."""
    model = Message
    template_name = 'messages/list.html'
    context_object_name = 'messages'
    paginate_by = 20

    def get_queryset(self):
        from apps.businesses.models import Business
        try:
            business = Business.objects.get(owner=self.request.user)
            return Message.objects.filter(business=business)
        except Business.DoesNotExist:
            return Message.objects.none()


@method_decorator(login_required, name='dispatch')
class MessageDetailView(DetailView):
    """View message details."""
    model = Message
    template_name = 'messages/detail.html'
    context_object_name = 'message'
