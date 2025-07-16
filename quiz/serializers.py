from rest_framework import serializers
from .models import UserProfile, Quiz, QuizSession
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from quiz.models import UserProfile

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

class CustomRegisterSerializer(BaseUserCreateSerializer):
    name = serializers.CharField(required=False, allow_blank=True)
    number = serializers.CharField(required=False, allow_blank=True)
    school = serializers.CharField(required=False, allow_blank=True)
    tutor_name = serializers.CharField(required=False, allow_blank=True)
    tutor_number = serializers.CharField(required=False, allow_blank=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password', 'name', 'number', 'school', 'tutor_name', 'tutor_number')

    def create(self, validated_data):
        name = validated_data.pop("name", "")
        number = validated_data.pop("number", "")
        school = validated_data.pop("school", "")
        tutor_name = validated_data.pop("tutor_name", "")
        tutor_number = validated_data.pop("tutor_number", "")

        user = super().create(validated_data)
        UserProfile.objects.create(
            user=user,
            name=name,
            number=number,
            school=school,
            tutor_name=tutor_name,
            tutor_number=tutor_number,
        )
        
        return user 
    
class CustomLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }

        return data