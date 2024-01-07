from django.db import router
from django.urls import path

from courses.views import LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView, CourseViewSet, PaymentListAPIView, PaymentCreateAPIView, PaymentRetrieveAPIView

from courses.apps import CoursesConfig
app_name=CoursesConfig.name

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')


urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='create_lesson'),
    path('lesson/', LessonListAPIView.as_view(), name='list_lesson'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='get_lesson'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update_lesson'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='delete_lesson'),

    path('payment/create/', PaymentCreateAPIView.as_view(), name='create_payment'),
    path('payment/', PaymentListAPIView.as_view(), name='list_payment'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='get_payment'),
              ] + router.urls