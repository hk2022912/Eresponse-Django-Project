# accounts/urls.py
from django.urls import path
from .views import register, LoginView, ProtectedView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]
