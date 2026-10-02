from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Business, BusinessHours, ReceptionistConfig, EscalationConfig
from .forms import BusinessForm, BusinessHoursForm, ReceptionistConfigForm, EscalationConfigForm


@method_decorator(login_required, name='dispatch')
class BusinessCreateView(CreateView):
    """Create a new business."""
    model = Business
    form_class = BusinessForm
    template_name = 'businesses/create.html'
    success_url = reverse_lazy('dashboard:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        
        # Create default business hours
        for day in BusinessHours.Day.values:
            BusinessHours.objects.create(
                business=self.object,
                day=day,
                is_open=day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
                open_time='09:00',
                close_time='18:00'
            )
        
        # Create default receptionist config
        ReceptionistConfig.objects.create(business=self.object)
        
        # Create default escalation config
        EscalationConfig.objects.create(
            business=self.object,
            owner_email=self.request.user.email
        )
        
        messages.success(self.request, 'Business created successfully!')
        return response


@method_decorator(login_required, name='dispatch')
class BusinessDetailView(DetailView):
    """View business details."""
    model = Business
    template_name = 'businesses/detail.html'
    context_object_name = 'business'

    def get_queryset(self):
        return Business.objects.filter(owner=self.request.user)


@method_decorator(login_required, name='dispatch')
class BusinessUpdateView(UpdateView):
    """Update business details."""
    model = Business
    form_class = BusinessForm
    template_name = 'businesses/edit.html'
    success_url = reverse_lazy('dashboard:home')

    def get_queryset(self):
        return Business.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Business updated successfully!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BusinessHoursView(TemplateView):
    """Manage business hours."""
    template_name = 'businesses/hours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = get_object_or_404(Business, pk=self.kwargs['pk'], owner=self.request.user)
        context['business'] = business
        context['business_hours'] = business.business_hours.all()
        return context

    def post(self, request, *args, **kwargs):
        business = get_object_or_404(Business, pk=self.kwargs['pk'], owner=self.request.user)
        
        for day in BusinessHours.Day.values:
            hours = business.business_hours.get(day=day)
            hours.is_open = request.POST.get(f'{day}_is_open') == 'on'
            if hours.is_open:
                hours.open_time = request.POST.get(f'{day}_open_time', '09:00')
                hours.close_time = request.POST.get(f'{day}_close_time', '18:00')
            hours.save()
        
        messages.success(request, 'Business hours updated successfully!')
        return redirect('businesses:hours', pk=business.pk)


@method_decorator(login_required, name='dispatch')
class ReceptionistConfigView(UpdateView):
    """Configure AI receptionist."""
    model = ReceptionistConfig
    form_class = ReceptionistConfigForm
    template_name = 'businesses/receptionist.html'
    success_url = reverse_lazy('dashboard:home')

    def get_object(self):
        business = get_object_or_404(Business, pk=self.kwargs['pk'], owner=self.request.user)
        return get_object_or_404(ReceptionistConfig, business=business)

    def form_valid(self, form):
        messages.success(self.request, 'Receptionist configuration updated successfully!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class EscalationConfigView(UpdateView):
    """Configure escalation settings."""
    model = EscalationConfig
    form_class = EscalationConfigForm
    template_name = 'businesses/escalation.html'
    success_url = reverse_lazy('dashboard:home')

    def get_object(self):
        business = get_object_or_404(Business, pk=self.kwargs['pk'], owner=self.request.user)
        return get_object_or_404(EscalationConfig, business=business)

    def form_valid(self, form):
        messages.success(self.request, 'Escalation configuration updated successfully!')
        return super().form_valid(form)
