from celery import shared_task
from django.core.mail import send_mail

from courses.models import Course

import datetime
from django.utils import timezone

from users.models import User
from django.conf import settings

def send_mails(emails, subject, message, from_email):

    send_mail(subject,
              message,
              from_email,
              recipient_list=emails,
              fail_silently=False
              )

    @shared_task
    def check_update():
        recipient_email = 'my_test@mail.ru'
        for c in Course.objects.all():
            if c.last_update > c.last_view:
                send_mail(
                    subject='Информация о курсе',
                    message=f'Курс был обновлен!',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient_email]

                )
                c.last_view = c.last_update
                c.save()

    @shared_task
    def check_last_login():
        now = timezone.now()
        for user in User.objects.all():
            count_days = now - user.last_login.replace(tzinfo=timezone.utc)
            if count_days > datetime.timedelta(days=30):
                user.is_active = False
                user.save()