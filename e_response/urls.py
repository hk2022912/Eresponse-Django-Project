# e_response/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),              # default auth
    path('auth/', include('djoser.urls.authtoken')),     # token auth
    path('auth/', include('accounts.urls')),             # ✅ your custom auth views like register
    path('api/', include('accounts.urls')),              # ✅ same views under /api/ if needed
]
