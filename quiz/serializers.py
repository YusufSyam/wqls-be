from rest_framework import serializers
from .models import UserProfile, Quiz, QuizSession
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'name', 'number', 'school', 'tutor_name', 'tutor_number']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'bidang', 'start_date', 'end_date']

class QuizSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    quiz = QuizSerializer()

    class Meta:
        model = QuizSession
        fields = ['id', 'user', 'quiz', 'score', 'duration', 'user_start', 'user_end']
