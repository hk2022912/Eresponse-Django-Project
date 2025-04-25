from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from .serializers import UserRegistrationSerializer
from .models import CustomUser  # Your Custom User
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

# Register View (User Registration)
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = CustomUser.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Invalid request method."}, status=status.HTTP_400_BAD_REQUEST)


# Login View (Session-based)
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid username or password.')

        login(request, user)

        return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)



# Protected view example
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access!"})
