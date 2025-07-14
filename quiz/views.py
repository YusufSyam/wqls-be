from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .models import UserProfile, Quiz, QuizSession
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    QuizSerializer,
    QuizSessionSerializer
)

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
