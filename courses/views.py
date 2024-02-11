from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from config import settings
from courses.models import Course, Lesson, Payment, Subscription
from courses.paginators import CoursePaginator, LessonPagination
from courses.permissions import IsModerator, IsOwner, IsNotModerator
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer, \
    SubscriptionListSerializer

from courses.tasks import send_mails

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsOwner | IsModerator | IsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsNotModerator]
        elif self.action == 'destroy':
            permission_classes = [IsOwner | IsNotModerator]
        elif self.action == 'update':
            permission_classes = [IsOwner | IsModerator | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        pk = self.kwargs.get('pk')
        course = Course.objects.get(pk=pk)
        subscriptions = Subscription.objects.filter(course=course, is_active=True)
        from_email = settings.EMAIL_HOST_USER
        emails = list(subscriptions.values_list('user__email', flat=True))

        send_mails(emails, 'Course updated', 'Course updated', from_email)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser|IsAuthenticated]
    pagination_class = LessonPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator | IsAdminUser]

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator | IsAdminUser]

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsAdminUser]

#Payments
class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'pay_method')
    ordering_fields = ('date',)

class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        for subscription in Subscription.objects.filter(user=self.request.user):
            if subscription.course.id == request.data.get('course'):
                raise PermissionDenied('У вас уже есть подписка на этот курс.')
        if int(self.request.user.id) != int(request.data.get('user')):
            raise PermissionDenied('Нельзя оформлять подписки на другого пользователя.')

        return super().create(request, *args, **kwargs)


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


