
from django.core.mail import send_mail

def send_mails(emails, subject, message, from_email):

    send_mail(subject,
              message,
              from_email,
              recipient_list=emails,
              fail_silently=False
              )