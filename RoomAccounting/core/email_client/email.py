
from django.core.mail import send_mail as _send_mail
from django.core.mail import EmailMultiAlternatives as _Email

from core.settings import DEFAULT_FROM_EMAIL


def send_html_email(subject, message, to_list, html_content):
    email_obj = _Email(
        subject=subject,
        body=message,
        from_email=DEFAULT_FROM_EMAIL,
        to=to_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()


def send_text_email(subject, message, to_list):
    _send_mail(
        subject=subject,
        message=message,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=to_list)
