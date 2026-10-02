from django.urls import path
from . import api_views

app_name = 'accounts'

urlpatterns = [
    path('login/', api_views.LoginAPIView.as_view(), name='api_login'),
    path('logout/', api_views.LogoutAPIView.as_view(), name='api_logout'),
    path('register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('profile/', api_views.ProfileAPIView.as_view(), name='api_profile'),
    path('change-password/', api_views.ChangePasswordAPIView.as_view(), name='api_change_password'),
]
