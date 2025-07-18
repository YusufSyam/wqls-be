from django.urls import path
from .views import (
    QuizLeaderboardView,
    QuizListWithStatsView,
    UserListView,
    UserProfileListCreateView,
    QuizListCreateView,
    QuizSessionListCreateView,
    MyProfileView, 
    LogoutView,
    QuizSubmissionHistoryView,
    SubmitQuizView
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('profiles/', UserProfileListCreateView.as_view(), name='userprofile-list'),
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list'),
    path('quiz-sessions/', QuizSessionListCreateView.as_view(), name='quizsession-list'),
    path('me/', MyProfileView.as_view(), name='my-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("leaderboard/<str:bidang>/", QuizLeaderboardView.as_view(), name="quiz-leaderboard"),
    path("history/", QuizSubmissionHistoryView.as_view(), name="submission-history"),
    path('submit/', SubmitQuizView.as_view(), name='submit-quiz'),
    path('quizzes-stats/', QuizListWithStatsView.as_view(), name='quiz-list-stats'),
]
