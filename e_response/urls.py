# e_response/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Built-in and Djoser auth
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # Your custom routes
    path('auth/', include('accounts.urls')),     # optional under auth/
    path('api/', include('accounts.urls')),      # optional under api/

    # ✅ Add this to catch email verification
    path('accounts/', include('accounts.urls')),  # ✅ Fix: this enables /accounts/verify/...
]
