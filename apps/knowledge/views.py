from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import FAQ, KnowledgeBaseEntry
from .forms import FAQForm, KnowledgeBaseEntryForm


@method_decorator(login_required, name='dispatch')
class FAQListView(ListView):
    """List all FAQs."""
    model = FAQ
    template_name = 'knowledge/faqs.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        from apps.businesses.models import Business
        try:
            business = Business.objects.get(owner=self.request.user)
            return FAQ.objects.filter(business=business)
        except Business.DoesNotExist:
            return FAQ.objects.none()


@method_decorator(login_required, name='dispatch')
class FAQCreateView(CreateView):
    """Create a new FAQ."""
    model = FAQ
    form_class = FAQForm
    template_name = 'knowledge/faq_form.html'
    success_url = reverse_lazy('knowledge:faqs')

    def form_valid(self, form):
        from apps.businesses.models import Business
        business = Business.objects.get(owner=self.request.user)
        form.instance.business = business
        messages.success(self.request, 'FAQ created successfully!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class FAQUpdateView(UpdateView):
    """Update an FAQ."""
    model = FAQ
    form_class = FAQForm
    template_name = 'knowledge/faq_form.html'
    success_url = reverse_lazy('knowledge:faqs')

    def form_valid(self, form):
        messages.success(self.request, 'FAQ updated successfully!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class FAQDeleteView(DeleteView):
    """Delete an FAQ."""
    model = FAQ
    template_name = 'knowledge/faq_delete.html'
    success_url = reverse_lazy('knowledge:faqs')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'FAQ deleted successfully!')
        return super().delete(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class KnowledgeBaseListView(ListView):
    """List all knowledge base entries."""
    model = KnowledgeBaseEntry
    template_name = 'knowledge/knowledge_base.html'
    context_object_name = 'entries'

    def get_queryset(self):
        from apps.businesses.models import Business
        try:
            business = Business.objects.get(owner=self.request.user)
            return KnowledgeBaseEntry.objects.filter(business=business)
        except Business.DoesNotExist:
            return KnowledgeBaseEntry.objects.none()


@method_decorator(login_required, name='dispatch')
class KnowledgeBaseCreateView(CreateView):
    """Create a new knowledge base entry."""
    model = KnowledgeBaseEntry
    form_class = KnowledgeBaseEntryForm
    template_name = 'knowledge/kb_form.html'
    success_url = reverse_lazy('knowledge:knowledge_base')

    def form_valid(self, form):
        from apps.businesses.models import Business
        business = Business.objects.get(owner=self.request.user)
        form.instance.business = business
        messages.success(self.request, 'Knowledge base entry created successfully!')
        return super().form_valid(form)
