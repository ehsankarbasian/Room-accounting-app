from apps.NotificationApp.core.service import MessageFactory

from apps.NotificationContribApp.notification_types import MessageType

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import User


class SecurityNotifications:
    
    @staticmethod
    def send_reset_password(user: User, email: str, token: str):
        context = {'token': token, 'identifier': email}
        sender = MessageFactory.get_sender(user, MessageType.RESET_PASSWORD, context)
        sender.send()
