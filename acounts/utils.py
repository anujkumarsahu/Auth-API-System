from django.core.mail import EmailMessage
import os

class EmailUtils:
    @staticmethod
    def send_email(data):
        try:
            email = EmailMessage(
                subject=data['subject'],
                body=data['message'],
                from_email=os.environ.get('EMAIL_FROM'),
                to=[data['to']],
            )
            email.send(fail_silently=False)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
