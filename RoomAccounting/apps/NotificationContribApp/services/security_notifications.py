from apps.NotificationApp.core.service import NotificationDispatcher

from apps.NotificationContribApp.notification_types import MessageType
from apps.NotificationContribApp.core.message_types.reset_password.data_model import ResetPasswordDataModel

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import User


class SecurityNotifications:
    
    @staticmethod
    def send_reset_password(user: User, token: str):
        data = ResetPasswordDataModel(reset_token=token, username=user.username)
        NotificationDispatcher.send(user, MessageType.RESET_PASSWORD, data)
