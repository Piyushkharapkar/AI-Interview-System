from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from .serializer import UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes


User = get_user_model()


@permission_classes([AllowAny])
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # User is created and saved
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(
                {"error": "Please provide both username and password."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"error": "No active user found with these login credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        # If authentication is successful, generate or fetch an auth token.
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
