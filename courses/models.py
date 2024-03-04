from django.db import models
from config import settings

NULLABLE = {'null': True, 'blank': True}

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(**NULLABLE, upload_to='courses/', verbose_name='Превью')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(**NULLABLE, upload_to='courses/', verbose_name='Превью')
    video_url = models.URLField(**NULLABLE, verbose_name='Ссылка на видео')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,verbose_name='Владелец')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='Курс')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
                                ('cash', 'Cash'),
                                ('card', 'Card'),
                            ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Пользователь')
    date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='Курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name='Урок')

    amount = models.IntegerField(verbose_name='Сумма оплаты')
    pay_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, **NULLABLE, verbose_name='Способ оплаты')

    #stripe
    session_id = models.TextField(verbose_name='id сессии',  **NULLABLE)
    is_paid = models.BooleanField(verbose_name='статус оплаты', default=False,  **NULLABLE)
    currency = models.CharField(max_length=10, default='RUB', verbose_name='валюта', **NULLABLE)


    def __str__(self):
        return f'{self.user} {self.amount}({self.method}) - {self.date}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('course', 'lesson', 'date', 'user')

class Subscription(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='активна')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.user}: {self.course} {self.is_active}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
