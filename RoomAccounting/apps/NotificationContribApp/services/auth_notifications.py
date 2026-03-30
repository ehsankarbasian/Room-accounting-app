from enum import Enum

from django.urls import reverse
from django.conf import settings

from apps.NotificationApp.dispatching import NotificationDispatcher
from apps.NotificationApp.models import NotificationChannelVerification

from apps.NotificationContribApp.notification_types import MessageType, SenderType
from apps.NotificationContribApp.messages import OtpMessage, VerifyChannelMessage

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
            MessageType.OTP,
            data,
            channel_override=channel_name,
            preferred_channels=[SenderType.BALE, SenderType.EMAIL],
        )

    @staticmethod
    def send_message_identifier_verification(recipient, channel):
        
        # TODO (security):
        # Store a hash of the verification token instead of the raw token.
        #
        # Current implementation stores the token in plaintext, which means
        # a database leak would allow attackers to immediately use verification links.
        #
        # Recommended improvement:
        #   - Generate a random token
        #   - Store SHA256(token) in the database
        #   - Send the raw token in the verification URL
        #   - When verifying, hash the incoming token and compare
        #
        # This follows the same pattern used in password reset token systems
        # and prevents token reuse in case of database compromise.

        verification = NotificationChannelVerification.create_for_channel(channel)

        verification_url = _build_verification_url(
            verification.token
        )

        data = VerifyChannelMessage.Data(
            verification_url=verification_url
        )

        NotificationDispatcher.send(
            recipient,
            MessageType.CHANNEL_VERIFICATION,
            data,
        )
