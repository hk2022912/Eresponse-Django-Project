# accounts/urls.py
from django.urls import path
from .views import (
    register, LoginView, ProtectedView, ProfileView,
    request_password_reset, verify_otp, reset_password_final,verify_email
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify-email'),
     path('request-password-reset/', request_password_reset, name='request-password-reset'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('reset-password-final/', reset_password_final, name='reset-password-final'),
    
]
