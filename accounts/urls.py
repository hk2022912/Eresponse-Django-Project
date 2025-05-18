from django.urls import path
from .views import (
    LoginView, login_view, register, ProtectedView, ProfileView,
    request_password_reset, verify_otp, reset_password_final, verify_email,
    homepage_view  # ✅ Now correctly imported
)

urlpatterns = [
    # Template-based login page
    path('login-page/', login_view, name='login_page'),

    # Home page view
    path('homepage/', homepage_view, name='homepage'),

    path('register/', register, name='register'),

    # API login view
    path('login/', LoginView.as_view(), name='api_login'),

    path('protected/', ProtectedView.as_view(), name='protected'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify-email'),
    path('request-password-reset/', request_password_reset, name='request-password-reset'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('reset-password-final/', reset_password_final, name='reset-password-final'),
]
