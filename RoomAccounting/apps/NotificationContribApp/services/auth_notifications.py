from enum import Enum

from django.urls import reverse
from django.conf import settings

from apps.NotificationApp.dispatching import NotificationDispatcher

from apps.NotificationContribApp.messages import OtpMessage

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from apps.ReportApp.models import User


# Helper function
def _build_verification_url(token: str) -> str:

    path = reverse(
        "notifications:verify-channel",
        kwargs={"token": token},
    )

    return f"{settings.BASE_URL}{path}"


class AuthNotifications:
    """
    Notification service responsible for authentication-related messages.

    This layer acts as an application-level orchestration layer. It prepares
    message data objects and delegates delivery to the NotificationDispatcher.
    """

    @staticmethod
    def send_otp(user: "User", code: str, *, channel_name: Optional[Enum] = None):
        """
        Send a one-time password (OTP) notification to a user.

        channel_name : Optional[Enum]
            Optional channel override (e.g. SenderType.SMS).
            If provided, dispatcher will attempt to use that channel first.
        """

        data = OtpMessage.Data(code=code)

        NotificationDispatcher.send(
            user,
            OtpMessage,
            data,
            channel_override=channel_name,
            preferred_channels=['bale', 'email', 'terminal'],
        )
