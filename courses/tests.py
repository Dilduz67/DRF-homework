
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create(
            email='dgango_test@mail.ru',
            is_staff=True,
            is_active=True,
            is_superuser=False,
            first_name='Ivan',
            last_name='Ivanov'

        )
        self.owner.set_password('password')
        self.owner.save()
        self.client.force_authenticate(user=self.owner)

        self.course = Course.objects.create(title='test', description='test',)
        self.lesson = Lesson.objects.create(
            title='test lesson',
            description='test description',
            preview=None,
            video_url='https://youtube.com',
            owner=self.owner,
            course=self.course
            )

    def test_lesson_retrieve(self):
        response = self.client.get('/lesson/', args=[self.lesson.id])
        d=[{'id': self.lesson.id,
                          'title': self.lesson.title,
                          'description': self.lesson.description,
                          'preview': self.lesson.preview.name,
                          'video_url': self.lesson.video_url,
                          'owner' : self.lesson.owner.id,
                          'course': self.lesson.course.id,
                          }]
        self.assertEqual(response.status_code, status.HTTP_200_OK )
        self.assertEqual(response.json(),d)

    def test_lesson_create(self):
        response = self.client.post('/lesson/create/',
            data={'pk': 1, 'title': 'test 1', 'description': 'test 1', 'course': self.course.pk, 'owner': self.owner.id, 'video_url': 'https://youtube.com'}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertTrue(Lesson.objects.all().exists())

    def test_lesson_delete(self):
        response = self.client.delete(f'/lesson/delete/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_lesson_update(self):
        data = {
            'title': 'Changed title',
            'description': 'Changed description',
        }

        response = self.client.put(f'/lesson/update/{self.lesson.id}/',data=data)
        d={'id': self.lesson.id,
                          'title': data['title'],
                          'description': data['description'],
                          'preview': self.lesson.preview.name,
                          'video_url': self.lesson.video_url,
                          'owner' : self.lesson.owner.id,
                          'course': self.lesson.course.id,
                          }

        self.assertEquals(response.json(),d)


class SubscribeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='dgango_test@mail.ru',
            is_staff=True,
            is_active=True,
            is_superuser=False,
            first_name='Ivan',
            last_name='Ivanov'

        )
        self.user.set_password('password')
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(title='test', description='test course',)

        self.subscription = Subscription.objects.create(
            user=self.user,
            is_active=True,
            course=self.course
        )

    def test_subscription_create(self):
        self.client.post(
            '/subscription/create/',
            data={'user': self.user.pk, 'is_active': True, 'course': self.course.pk}
        )

        self.assertEqual(Subscription.objects.count(), 2)
        self.assertTrue(Subscription.objects.all().exists())


    def test_subscription_list(self):
        response = self.client.get('/subscription/', args=[self.subscription.id])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        d=[{'id': self.subscription.id, 'user': self.user.email, 'course': self.course.title}]
        self.assertEquals(response.json(),d)


    def test_subscription_delete(self):
        response = self.client.delete(f'/subscription/delete/{self.subscription.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

