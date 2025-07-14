from django.contrib import admin
from .models import UserProfile, Quiz, QuizSession

admin.site.register(UserProfile)
admin.site.register(Quiz)
admin.site.register(QuizSession)
