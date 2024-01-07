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
                                (1, 'Наличные'),
                                (2, 'Перевод'),
                            ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Пользователь')
    date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='Курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name='Урок')

    amount = models.IntegerField(verbose_name='Сумма оплаты')
    pay_method = models.IntegerField(choices=PAYMENT_METHOD_CHOICES, **NULLABLE, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.user} {self.amount}({self.method}) - {self.date}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('course', 'lesson', 'date', 'user')