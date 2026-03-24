from django.core.mail import EmailMultiAlternatives as _Email

from core.settings import DEFAULT_FROM_EMAIL

from apps.NotificationApp.registry import SenderRegistry
from apps.NotificationApp.interfaces import MessageSenderInterface

from apps.NotificationContribApp.message_schema import CanonicalMessage
from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(SenderType.EMAIL)
class EmailSender(MessageSenderInterface):
    """
    Email sender implementation using Django's email backend.
    """

    @staticmethod
    def render_payload(message: CanonicalMessage) -> dict:
        """
        Convert CanonicalMessage into an email payload.
        """

        return {
            "subject": "reset password",
            "html_content": message.text,
            "text_content": "message",
        }


    @staticmethod
    def send_payload(identifier: str, payload: dict) -> None:
        """
        Send email using Django's EmailMultiAlternatives.
        """

        email_obj = _Email(
            subject=payload["subject"],
            body=payload["text_content"],
            from_email=DEFAULT_FROM_EMAIL,
            to=[identifier],
        )

        email_obj.attach_alternative(
            payload["html_content"],
            "text/html",
        )

        email_obj.send()
