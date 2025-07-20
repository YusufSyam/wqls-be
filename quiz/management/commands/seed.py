from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz.models import UserProfile, Quiz, QuizSession, Bidang
from faker import Faker
import random
from datetime import timedelta

fake = Faker()
userCount= 10000
quizSessionCount= 20000

class Command(BaseCommand):
    help = 'Seed database with dummy users, quizzes, and quiz sessions using bulk_create'

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Seeding data with bulk_create...")

        # Create Quiz objects for all subjects
        bidang_choices = [b[0] for b in Bidang.choices]
        quiz_list = []
        for bidang in bidang_choices:
            quiz_list.append(
                Quiz(
                    title=f"Kuis Mingguan - {bidang}",
                    bidang=bidang,
                    start_date=fake.date_time_this_year(),
                    end_date=fake.date_time_this_year()
                )
            )
        Quiz.objects.bulk_create(quiz_list, ignore_conflicts=True)
        self.stdout.write(f"✔ Created {len(bidang_choices)} quiz")

        quizzes = list(Quiz.objects.all())

        # Generate 10,000 Users + UserProfiles
        user_list = []
        for i in range(userCount):
            username = fake.user_name() + str(i)
            email = fake.email()
            user = User(username=username, email=email)
            user.set_password('password123')
            user_list.append(user)

            if(i%100==0):
                print(f'{i} user generated..')

        User.objects.bulk_create(user_list)
        self.stdout.write("Created 10,000 users")

        # Get saved users (with IDs)
        users = list(User.objects.all())

        # Create UserProfile
        profile_list = []
        for user in users:
            profile_list.append(
                UserProfile(
                    user=user,
                    name=fake.name(),
                    number=fake.phone_number(),
                    school=fake.company(),
                    tutor_name=fake.name(),
                    tutor_number=fake.phone_number()
                )
            )
        UserProfile.objects.bulk_create(profile_list)
        self.stdout.write("Success created 10,000 user profiles")

        # Create 20,000 QuizSession
        session_list = []
        for i in range(quizSessionCount):
            user = random.choice(users)
            quiz = random.choice(quizzes)
            start = fake.date_time_this_year()
            end = start + timedelta(minutes=random.randint(5, 60))
            duration = int((end - start).total_seconds())

            session_list.append(
                QuizSession(
                    user=user,
                    quiz=quiz,
                    score=random.randint(0, 100),
                    duration=duration,
                    user_start=start,
                    user_end=end
                )
            )
            
            if(i%100==0):
                print(f'{i} quiz generated..')

        QuizSession.objects.bulk_create(session_list)
        self.stdout.write("Success created 20,000 quiz submissions")

        self.stdout.write(self.style.SUCCESS("🎉 Done seeding all dummy data!"))