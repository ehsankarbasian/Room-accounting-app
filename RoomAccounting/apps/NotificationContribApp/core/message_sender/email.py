from django.core.mail import EmailMultiAlternatives as _Email

from core.settings import DEFAULT_FROM_EMAIL

from apps.NotificationApp.core.registry import SenderRegistry
from apps.NotificationApp.core.interfaces import MessageSenderInterface

from apps.NotificationContribApp.core.models.canonical import NotificationCanonicalMessage
from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(name=SenderType.EMAIL)
class EmailSender(MessageSenderInterface):

    def __init__(self, identifier):
        self._to = identifier

    def render_payload(self, message: NotificationCanonicalMessage):

        payload = {
            "subject": "reset password",
            "html_content": message.text,
            "text_content": "message"
        }

        return payload


    def send(self, payload):
        
        print(payload)

        email_obj = _Email(
            subject=payload["subject"],
            body=payload["text_content"],
            from_email=DEFAULT_FROM_EMAIL,
            to=[self._to],
        )

        email_obj.attach_alternative(
            payload["html_content"],
            "text/html"
        )

        email_obj.send()
