from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer,EmployeeProfileSerializer,ChangePasswordSerializer,EmployeeviewPositionSerializer,EmployeeProfilePicSerializer
from rest_framework.permissions import AllowAny
from django.utils import timezone
from rest_framework.views import APIView
from .utils import get_tokens
from django.contrib.auth import authenticate
from rest_framework import viewsets
from .models import CustomUser,EmployeeProfile
from Permission import IsEmployeeUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from admin_app.models import Position
from admin_app.serializers import PositionSerializer
import os

class RegisterView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow access to unauthenticated users

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        


        # Update last login timestamp
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        # Serialize user data
        serialized_data = CustomUserSerializer(user).data
        user_id = serialized_data['id']
        # Generate JWT token
        token = get_tokens(user)
        
        # Create response with HTTP-only cookie for the token
        return Response({
            "user_id":user_id,
            'token': token,
            'user_role': 'admin' if user.is_superuser else 'Employee',
            'message': 'Successfully logged in'
        })
    
        response.set_cookie(key='jwt', value=token, httponly=True)

        return response
    

# checking the admin url for admin access items


class EmployeeView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsEmployeeUser]

    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user
        
        # Return only the data of the authenticated user
        return CustomUser.objects.filter(id=user.id, is_superuser=False)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        # Optionally, add logic here to handle custom deletion behavior
        instance.delete()


    
# api for change password
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        update_session_auth_hash(request, user)  # Important!

        return Response({"detail": "Password has been changed successfully."}, status=status.HTTP_200_OK)
    


class EmployeePositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = EmployeeviewPositionSerializer
    permission_classes = [IsEmployeeUser]

class PostionView(APIView):
    def get(self, request):
        positions = Position.objects.all()  # Query all Position objects
        serializer = PositionSerializer(positions, many=True)  # Serialize the queryset
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data
    

class EmployeeProfileImageUpload(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            profile = EmployeeProfile.objects.get(user=request.user)
        except EmployeeProfile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeProfilePicSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            profile = EmployeeProfile.objects.get(user=request.user)
        except EmployeeProfile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if there's an existing image and delete it
        if profile.profile_image:
            old_image_path = profile.profile_image.path
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)

        serializer = EmployeeProfilePicSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)