from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Contact
from .forms import ContactForm


@method_decorator(login_required, name='dispatch')
class ContactListView(ListView):
    """List all contacts."""
    model = Contact
    template_name = 'contacts/list.html'
    context_object_name = 'contacts'
    paginate_by = 20

    def get_queryset(self):
        from apps.businesses.models import Business
        try:
            business = Business.objects.get(owner=self.request.user)
            return Contact.objects.filter(business=business)
        except Business.DoesNotExist:
            return Contact.objects.none()


@method_decorator(login_required, name='dispatch')
class ContactCreateView(CreateView):
    """Create a new contact."""
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/create.html'
    success_url = reverse_lazy('contacts:list')

    def form_valid(self, form):
        from apps.businesses.models import Business
        business = Business.objects.get(owner=self.request.user)
        form.instance.business = business
        messages.success(self.request, 'Contact created successfully!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ContactDetailView(DetailView):
    """View contact details."""
    model = Contact
    template_name = 'contacts/detail.html'
    context_object_name = 'contact'


@method_decorator(login_required, name='dispatch')
class ContactUpdateView(UpdateView):
    """Update contact details."""
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/edit.html'
    success_url = reverse_lazy('contacts:list')

    def form_valid(self, form):
        messages.success(self.request, 'Contact updated successfully!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ContactDeleteView(DeleteView):
    """Delete a contact."""
    model = Contact
    template_name = 'contacts/delete.html'
    success_url = reverse_lazy('contacts:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Contact deleted successfully!')
        return super().delete(request, *args, **kwargs)
