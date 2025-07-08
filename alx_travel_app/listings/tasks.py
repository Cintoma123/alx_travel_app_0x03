from celery import celery , shared_task
from django.core.email import EmailMessage
@shared_task
def send_email_message(sender , reciever, message):
    mail = "You have sucessfullly makes a booking"
    message_subject = "hello  your booking is reading kindly wait for booking  to be processed" .format(
        sender , reciever , message)
    email = EmailMessage(mail , message_subject to=[])
    email.send()