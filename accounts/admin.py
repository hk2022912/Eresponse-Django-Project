# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # now properly imported

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'age', 'contact_number']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'contact_number']
    ordering = ['email']

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('age', 'contact_number')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('age', 'contact_number')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
