from django.urls import path
from .views import register, LoginView

urlpatterns = [
    path('register/', register, name='register'),  # User Registration endpoint
    path('login/', LoginView.as_view(), name='login'),  # User Login endpoint
]
