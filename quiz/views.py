from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, Quiz, QuizSession
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    QuizSerializer,
    QuizSessionSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken

# User (readonly)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# UserProfile
class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# Quiz
class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

# QuizSession
class QuizSessionListCreateView(generics.ListCreateAPIView):
    queryset = QuizSession.objects.select_related('user', 'quiz').all()
    serializer_class = QuizSessionSerializer

class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"message": f"Hello, {user.username}!"})
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # <-- Pastikan blacklist diaktifkan
            return Response(status=204)
        except Exception as e:
            return Response(status=400)