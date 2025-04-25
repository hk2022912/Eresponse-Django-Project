from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),              # /auth/users/
    path('auth/', include('djoser.urls.authtoken')),    # /auth/token/login
    path('auth/', include('accounts.urls')),            # Your custom user logic
    path('api/', include('accounts.urls')),             # ✅ Custom login route like /api/login/
]
