from rest_framework import serializers
from .models import UserProfile, Quiz, QuizSession
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from quiz.models import UserProfile, QuizSession

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
    

class QuizSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSession
        fields = ["id", "quiz", "score", "duration", "user_end", "user_start"] 


class QuizSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSession
        fields = ['quiz', 'score', 'user_start', 'user_end']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['duration'] = int((validated_data['user_end'] - validated_data['user_start']).total_seconds())
        return super().create(validated_data)
    
    
class QuizWithStatsSerializer(serializers.ModelSerializer):
    total_submissions = serializers.SerializerMethodField()
    user_submissions = serializers.SerializerMethodField()
    user_best_rank = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'bidang', 'start_date', 'end_date', 
                  'total_submissions', 'user_submissions', 'user_best_rank']

    def get_total_submissions(self, obj):
        return QuizSession.objects.filter(quiz=obj).count()

    def get_user_submissions(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return QuizSession.objects.filter(user=user, quiz=obj).count()
        return None

    def get_user_best_rank(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return None

        # Ambil semua session untuk quiz ini
        all_sessions = QuizSession.objects.filter(quiz=obj).order_by('-score', 'duration', 'user_end')
        user_sessions = all_sessions.filter(user=user)

        if not user_sessions.exists():
            return None

        # Cari rank tertinggi user
        user_best_rank = None
        for idx, session in enumerate(all_sessions, start=1):
            if session.user == user:
                if user_best_rank is None or idx < user_best_rank:
                    user_best_rank = idx
        return user_best_rank
