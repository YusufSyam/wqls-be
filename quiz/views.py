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
from .serializers import LeaderboardEntrySerializer
from rest_framework import status

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
        

class LeaderboardView(APIView):
    def get(self, request):
        bidang = request.query_params.get('bidang')
        if not bidang:
            return Response({"error": "Parameter 'bidang' harus diberikan."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quiz = Quiz.objects.get(bidang=bidang)
        except Quiz.DoesNotExist:
            return Response({"error": f"Tidak ada quiz dengan bidang '{bidang}'"}, status=status.HTTP_404_NOT_FOUND)

        sessions = QuizSession.objects.filter(quiz=quiz).order_by('-score', 'duration')[:10]  # Top 10
        serializer = LeaderboardEntrySerializer(sessions, many=True)
        return Response(serializer.data)