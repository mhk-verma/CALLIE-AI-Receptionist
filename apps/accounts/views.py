from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import timedelta
from .models import User, PasswordReset, EmailVerification
from .forms import SignUpForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, ProfileForm
import secrets


class SignUpView(CreateView):
    """User registration view."""
    model = User
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Create email verification token
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=24)
        EmailVerification.objects.create(
            user=self.object,
            token=token,
            expires_at=expires_at
        )
        
        # TODO: Send verification email
        messages.success(
            self.request,
            'Account created successfully! Please check your email to verify your account.'
        )
        return response


class LoginView(FormView):
    """User login view."""
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('dashboard:home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f'Welcome back, {user.get_full_name()}!')
        
        # Redirect to onboarding if not completed
        if not user.onboarding_completed:
            return redirect('accounts:onboarding')
        
        return super().form_valid(form)


class LogoutView(TemplateView):
    """User logout view."""
    template_name = 'accounts/logout.html'

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('accounts:login')


class ForgotPasswordView(FormView):
    """Forgot password view."""
    form_class = ForgotPasswordForm
    template_name = 'accounts/forgot_password.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            
            # Create password reset token
            token = secrets.token_urlsafe(32)
            expires_at = timezone.now() + timedelta(hours=1)
            PasswordReset.objects.create(
                user=user,
                token=token,
                expires_at=expires_at
            )
            
            # TODO: Send password reset email
            messages.success(
                self.request,
                'If an account exists with that email, you will receive password reset instructions.'
            )
        except User.DoesNotExist:
            messages.success(
                self.request,
                'If an account exists with that email, you will receive password reset instructions.'
            )
        
        return super().form_valid(form)


class ResetPasswordView(FormView):
    """Reset password view."""
    form_class = ResetPasswordForm
    template_name = 'accounts/reset_password.html'
    success_url = reverse_lazy('accounts:login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['token'] = self.kwargs['token']
        return kwargs

    def form_valid(self, form):
        password_reset = form.password_reset
        password_reset.user.set_password(form.cleaned_data['password'])
        password_reset.user.save()
        password_reset.used = True
        password_reset.save()
        
        messages.success(self.request, 'Your password has been reset successfully.')
        return super().form_valid(form)


class VerifyEmailView(TemplateView):
    """Email verification view."""
    template_name = 'accounts/verify_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.kwargs['token']
        
        try:
            verification = EmailVerification.objects.get(token=token)
            if verification.is_valid():
                verification.user.email_verified = True
                verification.user.save()
                verification.used = True
                verification.save()
                context['success'] = True
                messages.success(self.request, 'Your email has been verified successfully!')
            else:
                context['success'] = False
                context['message'] = 'This verification link has expired or already been used.'
        except EmailVerification.DoesNotExist:
            context['success'] = False
            context['message'] = 'Invalid verification link.'
        
        return context


@method_decorator(login_required, name='dispatch')
class ProfileView(UpdateView):
    """User profile view."""
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


class OnboardingView(TemplateView):
    """Onboarding wizard view."""
    template_name = 'accounts/onboarding.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = int(self.request.GET.get('step', 1))
        return context

    def post(self, request, *args, **kwargs):
        step = int(request.POST.get('step', 1))
        
        if step == 1:
            # Business information
            request.session['onboarding_business'] = {
                'name': request.POST.get('business_name'),
                'type': request.POST.get('business_type'),
                'phone': request.POST.get('phone'),
                'email': request.POST.get('email'),
                'address': request.POST.get('address'),
                'website': request.POST.get('website'),
                'description': request.POST.get('description'),
            }
            return redirect(f"{request.path}?step=2")
        
        elif step == 2:
            # Business hours
            request.session['onboarding_hours'] = request.POST.dict()
            return redirect(f"{request.path}?step=3")
        
        elif step == 3:
            # AI receptionist configuration
            request.session['onboarding_receptionist'] = {
                'name': request.POST.get('receptionist_name'),
                'personality': request.POST.get('personality'),
                'greeting': request.POST.get('greeting'),
                'language': request.POST.get('language'),
                'tone': request.POST.get('tone'),
            }
            return redirect(f"{request.path}?step=4")
        
        elif step == 4:
            # FAQs
            request.session['onboarding_faqs'] = request.POST.dict()
            return redirect(f"{request.path}?step=5")
        
        elif step == 5:
            # Escalation settings
            request.session['onboarding_escalation'] = {
                'emergency_contact': request.POST.get('emergency_contact'),
                'owner_email': request.POST.get('owner_email'),
                'urgent_keywords': request.POST.get('urgent_keywords'),
            }
            
            # Create business and complete onboarding
            # TODO: Implement business creation logic
            
            request.user.onboarding_completed = True
            request.user.save()
            
            messages.success(request, 'Onboarding completed successfully!')
            return redirect('dashboard:home')
        
        return redirect(f"{request.path}?step={step}")
