from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .serializers import UserRegistrationSerializer
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .utils import send_verification_email  # ⬅️ Add this
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

@csrf_exempt
@api_view(['POST'])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = CustomUser.objects.create_user(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email'),
            password=serializer.validated_data.get('password'),
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', ''),
            age=serializer.validated_data.get('age'),
            contact_number=serializer.validated_data.get('contact_number'),
            is_active=False  # ⬅️ Set inactive until verified
        )

        send_verification_email(request, user)  # ⬅️ Send email

        return Response({"message": "Registration successful! Please check your email to verify your account."}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View (Session-Based Authentication)
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            raise AuthenticationFailed('Username and password are required.')

        user = authenticate(request, username=username, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid username or password.')

        if not user.is_active:
            raise AuthenticationFailed('Please verify your email before logging in.')

        login(request, user)

        return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)



# Profile View (Displays user information from the session)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # The logged-in user
        user_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'contact_number': user.contact_number
        }
        return Response(user_data)

@api_view(['GET'])
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        return Response({"message": "Email successfully verified. You can now log in."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid or expired link."}, status=status.HTTP_400_BAD_REQUEST)
    
# Example Protected View (only logged-in users can access)
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access!"})