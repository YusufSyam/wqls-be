from django.db import models
from django.contrib.auth.models import User

class Bidang(models.TextChoices):
    ASTRONOMI = "Astronomi"
    BIOLOGI = "Biologi"
    EKONOMI = "Ekonomi"
    FISIKA = "Fisika"
    GEOGRAFI = "Geografi"
    INFORMATIKA = "Informatika"
    KEBUMIAN = "Kebumian"
    KIMIA = "Kimia"
    MATEMATIKA = "Matematika"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=30)
    school = models.CharField(max_length=100)
    tutor_name = models.CharField(max_length=100)
    tutor_number = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    bidang = models.CharField(max_length=30, choices=Bidang.choices)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title

class QuizSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    duration = models.PositiveIntegerField(help_text="Durasi dalam detik")
    user_start = models.DateTimeField()
    user_end = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score})"
