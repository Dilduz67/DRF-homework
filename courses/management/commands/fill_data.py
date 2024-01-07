import random
from decimal import Decimal

from django.core.management import BaseCommand

from courses.models import Payment, Lesson, Course
from users.models import User

import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        Payment.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()

        users = []
        for x in range(5):
            email = f'email{x}@test.ru'
            full_name = f'User {x}'
            user = User.objects.create(email=email,full_name=full_name)
            user.set_password(f'Password{x}')
            user.save()
            users.append(user)

        courses = []
        lessons = []
        for i in range(5):
            course = Course.objects.create(
                title= f'Course {i}',
                description=f'Description {i}',
                owner=users[i],
            )
            courses.append(course)

            for j in range(5):
                lesson = Lesson.objects.create(
                    title=f'Lesson {j}',
                    description=f'Description {j}',

                    course=course,
                    owner=users[i],
                )
                lessons.append(lesson)


        for x in range(20):
            user = random.choice(users)
            payment_date = datetime.datetime(2024, 1, x+1)
            amount = Decimal(random.uniform(10, 1000))
            payment_method = random.choice([1, 2])

            is_course = random.choice([True, False])
            course_or_lesson = random.choice(courses) if is_course else random.choice(lessons)

            Payment.objects.create(
                user=user,
                date=payment_date,
                course=course_or_lesson if is_course else None,
                lesson=course_or_lesson if not is_course else None,
                amount=amount,
                pay_method=payment_method,
            )