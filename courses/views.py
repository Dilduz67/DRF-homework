from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from courses.models import Course, Lesson, Payment
from courses.permissions import IsModerator, IsOwner, IsNotModerator
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

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


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]

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

