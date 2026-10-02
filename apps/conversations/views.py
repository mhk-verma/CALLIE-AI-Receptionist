from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import Conversation


@method_decorator(login_required, name='dispatch')
class ConversationListView(ListView):
    """List all conversations."""
    model = Conversation
    template_name = 'conversations/list.html'
    context_object_name = 'conversations'
    paginate_by = 20

    def get_queryset(self):
        from apps.businesses.models import Business
        try:
            business = Business.objects.get(owner=self.request.user)
            return Conversation.objects.filter(business=business)
        except Business.DoesNotExist:
            return Conversation.objects.none()


@method_decorator(login_required, name='dispatch')
class ConversationDetailView(DetailView):
    """View conversation details."""
    model = Conversation
    template_name = 'conversations/detail.html'
    context_object_name = 'conversation'
