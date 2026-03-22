from apps.NotificationApp.dispatcher import NotificationDispatcher

from apps.NotificationContribApp.notification_types import MessageType
from apps.NotificationContribApp.messages import ResetPasswordMessage

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import User


class SecurityNotifications:
    
    @staticmethod
    def send_reset_password(user: User, token: str):
        data = ResetPasswordMessage.Data(reset_token=token, username=user.username)
        NotificationDispatcher.send(user, MessageType.RESET_PASSWORD, data)
