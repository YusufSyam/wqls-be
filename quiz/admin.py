from django.contrib import admin
from .models import UserProfile, Quiz, QuizSession

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'number', 'school', 'tutor_name', 'tutor_number')
    search_fields = ('name', 'school', 'tutor_name')
    list_filter = ('school',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'bidang', 'start_date', 'end_date')
    list_filter = ('bidang',)
    search_fields = ('title',)

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'quiz', 'score', 'duration', 'user_start', 'user_end')
    list_filter = ('quiz__bidang',)
    search_fields = ('user__username',)
