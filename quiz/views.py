from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, Quiz, QuizSession, Bidang
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    QuizSerializer,
    QuizSessionSerializer,
    QuizSubmissionSerializer,
    QuizSessionCreateSerializer,
    QuizWithStatsSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.core.paginator import Paginator

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
        try:
            profile = user.userprofile
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "name": profile.name,
                "number": profile.number,
                "school": profile.school,
                "tutor_name": profile.tutor_name,
                "tutor_number": profile.tutor_number
            }
        except UserProfile.DoesNotExist:
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "error": "UserProfile not found."
            }

        return Response(data)
    
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
        
    
class QuizLeaderboardView(APIView):
    def get(self, request, bidang):
        try:
            bidang= bidang.capitalize()
            # Validasi bidang
            if bidang not in Bidang.values:
                return Response({"error": "Bidang tidak valid."}, status=status.HTTP_400_BAD_REQUEST)

            # Ambil quiz berdasarkan bidang
            try:
                quiz = Quiz.objects.get(bidang=bidang)
            except Quiz.DoesNotExist:
                return Response({"error": "Quiz tidak ditemukan untuk bidang tersebut."}, status=status.HTTP_404_NOT_FOUND)

            # Ambil parameter query: limit & offset
            limit = int(request.query_params.get("limit", 10))
            offset = int(request.query_params.get("offset", 0))

            # Ambil semua sesi quiz terkait, urutkan berdasarkan score desc dan duration asc
            sessions = QuizSession.objects.filter(quiz=quiz).select_related("user").order_by("-score", "duration")

            # Total data sebelum pagination
            total = sessions.count()

            # Terapkan offset dan limit (manual pagination)
            paginated_sessions = sessions[offset:offset+limit]

            # Buat response data
            leaderboard = []
            for i, session in enumerate(paginated_sessions, start=offset + 1):
                profile = getattr(session.user, 'userprofile', None)
                leaderboard.append({
                    "rank": i,
                    "username": session.user.username,
                    "name": profile.name if profile else "",
                    "school": profile.school if profile else "",
                    "score": session.score,
                    "duration": session.duration,
                    "subject": bidang
                })

            userRankList = []
            if request.user and request.user.is_authenticated:
                user_sessions = sessions.filter(user=request.user)

                for user_session in user_sessions:
                    # Hitung ranking untuk sesi ini
                    rank = 1 + sessions.filter(
                        score__gt=user_session.score
                    ).count() + sessions.filter(
                        score=user_session.score,
                        duration__lt=user_session.duration
                    ).count()

                    userRankList.append(rank)

            return Response({
                "total": total,
                "data": leaderboard,
                "userRankList": userRankList
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class QuizSubmissionHistoryView(generics.ListAPIView):
    serializer_class = QuizSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            QuizSession.objects.filter(user=self.request.user)
            .order_by("-user_end")  # ganti sesuai nama field timestamp kamu
        )
    
class SubmitQuizView(generics.CreateAPIView):
    queryset = QuizSession.objects.all()
    serializer_class = QuizSessionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class QuizListWithStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        quizzes = Quiz.objects.all().order_by('-start_date')
        serializer = QuizWithStatsSerializer(quizzes, many=True, context={'request': request})
        return Response(serializer.data)
    
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            return Response({"error": "UserProfile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "profile": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)