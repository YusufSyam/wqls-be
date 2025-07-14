from django.urls import path
from .views import (
    UserListView,
    UserProfileListCreateView,
    QuizListCreateView,
    QuizSessionListCreateView,
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('profiles/', UserProfileListCreateView.as_view(), name='userprofile-list'),
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list'),
    path('quiz-sessions/', QuizSessionListCreateView.as_view(), name='quizsession-list'),
]
