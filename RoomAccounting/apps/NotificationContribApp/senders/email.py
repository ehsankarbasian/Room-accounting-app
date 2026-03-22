from django.core.mail import EmailMultiAlternatives as _Email

from core.settings import DEFAULT_FROM_EMAIL

from apps.NotificationApp.registry import SenderRegistry
from apps.NotificationApp.interfaces import MessageSenderInterface

from apps.NotificationContribApp.messages.canonical import CanonicalMessage
from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(SenderType.EMAIL)
class EmailSender(MessageSenderInterface):

    @staticmethod
    def render_payload(message: CanonicalMessage) -> dict:

        payload = {
            "subject": "reset password",
            "html_content": message.text,
            "text_content": "message"
        }

        return payload


    @staticmethod
    def send_payload(identifier: str, payload: dict) -> None:
        
        print(payload)

        email_obj = _Email(
            subject=payload["subject"],
            body=payload["text_content"],
            from_email=DEFAULT_FROM_EMAIL,
            to=[identifier],
        )

        email_obj.attach_alternative(
            payload["html_content"],
            "text/html"
        )

        email_obj.send()
