import smtplib
from email.message import EmailMessage

from celery import Celery
from config import settings


celery = Celery('tasks', broker=settings.REDIS_URI)


def get_email_template_dashboard(key: str):
    email = EmailMessage()
    email['From'] = settings.SMTP_EMAIL
    email['To'] = settings.TEST_EMAIL

    email.set_content(f'Hi, {settings.SMTP_NAME}\nThe key is {key}')
    return email


@celery.task
def send_email_report_dashboard(key: str):
    email = get_email_template_dashboard(key=key)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_HOST) as server:
        server.login(settings.SMTP_LOGIN, settings.SMTP_PASSWORD)
        server.send_message(email)
