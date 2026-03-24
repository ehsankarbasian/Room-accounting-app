from apps.NotificationApp.dispatching import NotificationDispatcher

from apps.NotificationContribApp.notification_types import MessageType
from apps.NotificationContribApp.messages import ResetPasswordMessage

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from apps.ReportApp.models import User


class SecurityNotifications:
    """
    Notification service responsible for security-sensitive messages
    such as password resets or security alerts.
    """

    @staticmethod
    def send_reset_password(user: User, token: str):

        data = ResetPasswordMessage.Data(
            reset_token=token,
            username=user.username
        )

        NotificationDispatcher.send(
            user,
            MessageType.RESET_PASSWORD,
            data,
        )
