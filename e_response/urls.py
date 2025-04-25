from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),  # 🔄 this handles /auth/users/
    path('auth/', include('djoser.urls.authtoken')),  # 🔄 this handles login/logout
    path('auth/', include('accounts.urls')),  # Auth URLs
]
