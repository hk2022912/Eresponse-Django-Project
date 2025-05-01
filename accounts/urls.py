# accounts/urls.py
from django.urls import path
from .views import register, LoginView, ProtectedView, ProfileView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
     path('profile/', ProfileView.as_view(), name='profile'),  # Profile endpoint
]
