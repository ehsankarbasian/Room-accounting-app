from django.core.mail import EmailMultiAlternatives as _Email

from core.settings import DEFAULT_FROM_EMAIL

from apps.NotificationApp.interfaces import MessageSenderInterface
from apps.NotificationContribApp.message_schema import CanonicalMessage


class EmailSender(MessageSenderInterface):
    """
    Email sender implementation using Django's email backend.
    """
    
    sender_key = "email"

    @staticmethod
    def render_payload(message: CanonicalMessage) -> dict:
        """
        Convert CanonicalMessage into an email payload.
        """
        
        buttons_as_text = ""
        for button in message.buttons + message.button_links:
            buttons_as_text += f'\n{button.text}:\n{button.target}\n'

        return {
            "subject": "reset password",
            "html_content": message.text,
            "text_content": "message",
            "buttons_as_text": buttons_as_text,
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
        
        print("\n", "-" * 100)
        print("\nSending ...\n")

        print("Email payload: ", payload)
        print("Email object: ", email_obj)

        print("\nmessage receiver identifier:")
        print(f"    {identifier}")

        print("\n", "-" * 100, "\n")

        # email_obj.send()
