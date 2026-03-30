from enum import Enum

from NotificationApp.dispatching import NotificationDispatcher

from ..notification_types import MessageType, SenderType
from ..messages import OtpMessage

from typing import TYPE_CHECKING, Optional
# TODO: if TYPE_CHECKING:
#     from accounts_app.models import User


class AuthNotifications:
    """
    Notification service responsible for authentication-related messages.

    This layer acts as an application-level orchestration layer. It prepares
    message data objects and delegates delivery to the NotificationDispatcher.
    """

    @staticmethod
    def send_otp(
        user: "User",
        code: str,
        *,
        channel_name: Optional[Enum] = None
    ):
        """
        Send a one-time password (OTP) notification to a user.

        channel_name : Optional[Enum]
            Optional channel override (e.g. SenderType.SMS).
            If provided, dispatcher will attempt to use that channel first.
        """

        data = OtpMessage.Data(code=code)

        NotificationDispatcher.send(
            user,
            MessageType.OTP,
            data,
            channel_override=channel_name,
            preferred_channels=[SenderType.BALE, SenderType.EMAIL],
        )

    @staticmethod
    def send_message_identifier_verification(recipient):
        pass
