from NotificationApp.dispatching import NotificationDispatcher

from ..notification_types import MessageType
from ..messages import ResetPasswordMessage

from typing import TYPE_CHECKING
# TODO: if TYPE_CHECKING:
#     from accounts_app.models import User


class SecurityNotifications:
    """
    Notification service responsible for security-sensitive messages
    such as password resets or security alerts.
    """

    @staticmethod
    def send_reset_password(user: "User", token: str):

        data = ResetPasswordMessage.Data(
            reset_token=token,
            username=user.username
        )

        NotificationDispatcher.send(
            user,
            MessageType.RESET_PASSWORD,
            data,
        )
