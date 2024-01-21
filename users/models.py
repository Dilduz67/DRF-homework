from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import NULLABLE

class UserRoles(models.TextChoices):
    MEMBER = 'member'
    MODERATOR = 'moderator'

class User(AbstractUser):
    username = None
    full_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='Город', **NULLABLE)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    is_active = models.BooleanField(default=False, verbose_name='Активация')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
