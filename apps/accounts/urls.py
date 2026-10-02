from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<token>/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('verify-email/<token>/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('onboarding/', views.OnboardingView.as_view(), name='onboarding'),
]
