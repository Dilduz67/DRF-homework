from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer
from django.contrib.auth.hashers import make_password


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = super().perform_create(serializer)

        if user is not None:
            password = self.request.data['password']
            hashed_password = make_password(password)
            user.set_password(hashed_password)
            user.save()

        return user