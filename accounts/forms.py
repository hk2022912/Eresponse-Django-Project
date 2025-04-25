from django import forms
from .models import CustomUser  # Import your custom user model
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # Use the CustomUser model here
        fields = ['username', 'email', 'password1', 'password2']
