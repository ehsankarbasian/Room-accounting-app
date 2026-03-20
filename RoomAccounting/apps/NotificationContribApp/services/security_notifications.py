from apps.NotificationApp.core.service import MessageFactory

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import User


class SecurityNotifications:
    
    @staticmethod
    def send_reset_password(user: User, email: str, token: str):
        context = {'token': token, 'identifier': email}
        sender = MessageFactory.get_sender(user, "reset_password", context)
        sender.send()
