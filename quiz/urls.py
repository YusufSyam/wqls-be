from django.urls import path
from .views import (
    QuizLeaderboardView,
    UserListView,
    UserProfileListCreateView,
    QuizListCreateView,
    QuizSessionListCreateView,
    MyProfileView, 
    LogoutView,
    QuizSubmissionHistoryView
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('profiles/', UserProfileListCreateView.as_view(), name='userprofile-list'),
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list'),
    path('quiz-sessions/', QuizSessionListCreateView.as_view(), name='quizsession-list'),
    path('me/', MyProfileView.as_view(), name='my-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("leaderboard/<str:bidang>/", QuizLeaderboardView.as_view(), name="quiz-leaderboard"),
    path("submissions/history/", QuizSubmissionHistoryView.as_view(), name="submission-history"),
]
