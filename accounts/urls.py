from django.urls import path
from .views import register, LoginView, ProtectedView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),  # ✅ This must exist
    path('protected/', ProtectedView.as_view(), name='protected'),
]
