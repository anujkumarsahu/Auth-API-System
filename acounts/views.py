from django.shortcuts import render
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView

from authapi.renderers import Renderer
from .serializers import UserRegistrationSerializer,UserLoginSerializer, UserProfileSerializer,UserChangePasswordSerializer,PasswordResetSerializer,SetResetNewPasswordSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [Renderer]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        # if raise_exception=True, this line of code validate post data and if data is not valid then it will raise error
        # if serializer.is_valid(raise_exception=True): 
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            tokens =get_tokens_for_user(user)
            return Response({'tokens':tokens,'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes = [Renderer]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user =authenticate(email=email, password=password)
            tokens = get_tokens_for_user(user)
            if user is None:
                return Response({'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'tokens':tokens,'msg': 'Login Successful'}, status=status.HTTP_200_OK)
        # print(serializer.errors) ##check error in console
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'msg': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserChangePasswordView(APIView):
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    renderer_classes = [Renderer]
    def post(self, request, format = None):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


class SetResetNewPasswordView(APIView):
    def post(self, request, uid, token):  # ⬅️ Receives from URL
        serializer = SetResetNewPasswordSerializer(data=request.data,  context={'uid': uid, 'token': token} )
        # print("uid",uid)
        # print("token",token)
        # print("data",request.data)
        # print(serializer.is_valid(raise_exception=True)) ## check in console
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class UserLogoutView(APIView):
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'msg': 'Logout successful'}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'msg': 'User not logged in'}, status=status.HTTP_400_BAD_REQUEST)  