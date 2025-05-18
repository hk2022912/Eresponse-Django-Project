# views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from .serializers import UserRegistrationSerializer
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from .utils import send_verification_email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import get_user_model
import json
import random  # ✅ <-- THIS LINE FIXES THE ERROR

User = get_user_model()

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
            is_active=False
        )

        send_verification_email(request, user)

        return Response({"message": "Registration successful! Please check your email to verify your account."}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
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


@csrf_exempt
def request_password_reset(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            cache.set(f"otp_{email}", otp, timeout=300)
            send_mail(
                "Your OTP Code",
                f"Your OTP code is: {otp}",
                "no-reply@example.com",
                [email],
                fail_silently=False,
            )
            return JsonResponse({"message": "OTP sent to your email."})
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        otp_input = data.get('otp')
        otp_real = cache.get(f"otp_{email}")

        if otp_input == otp_real:
            token = str(random.randint(10000000, 99999999))
            cache.set(f"reset_token_{email}", token, timeout=600)
            return JsonResponse({"message": "OTP verified.", "token": token})
        return JsonResponse({"error": "Invalid or expired OTP."}, status=400)

@csrf_exempt
def reset_password_final(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        token = data.get("token")
        new_password = data.get("new_password")

        saved_token = cache.get(f"reset_token_{email}")
        if token == saved_token:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return JsonResponse({"message": "Password reset successful."})
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found."}, status=404)
        return JsonResponse({"error": "Invalid token."}, status=400)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access!"})
    

# accounts/views.py
from django.shortcuts import render

def homepage(request):
    return render(request, 'accounts/homepage.html')

from django.shortcuts import render

def login_view(request):
    return render(request, 'accounts/login.html')  # make sure this file exists

from django.shortcuts import render
from django.http import HttpResponse

# Add this view if not already present
def homepage_view(request):
    return HttpResponse("Welcome to the Homepage!")  # Simple plain text response
