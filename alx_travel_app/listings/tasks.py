from celery import shared_task
from django.core.mail import EmailMessage
import time

@shared_task
def send_email_message(sender, receiver, message):
    try:
        if not sender or not receiver:
            raise ValueError("Sender and receiver must be provided")
        if not message:
            raise ValueError("Message cannot be empty")
        mail_message = "You have successfully made a booking"
        email_subject = "Booking confirmation\n\n" + mail_message
        email = EmailMessage(
            subject=email_subject,
            body=mail_message,
            from_email=sender,
            to=[receiver]
        )
        email.send()
        print("Email sent successfully")
        time.sleep(5)
        return True
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        return False