from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.conf import settings


class EmailAgent:
    def __init__(self, to_emails, subject, html_content):
        self.from_email = settings.FROM_EMAIL
        self.to_emails = to_emails
        self.subject = subject
        self.html_content = html_content

    def send_email(self):
        message = Mail(
            from_email=self.from_email,
            to_emails=self.to_emails,
            subject=self.subject,
            html_content=self.html_content,
        )
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            sg.send(message)
            return True
        except Exception as e:
            print(e)
