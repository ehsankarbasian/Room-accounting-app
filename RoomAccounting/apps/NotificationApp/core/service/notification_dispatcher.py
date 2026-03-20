from .message_factory import MessageFactory

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import User


class NotificationDispatcher:
    
    @staticmethod
    def send(user: User, message_type: str, context: dict):
        
        sender = MessageFactory.get_sender(
            user=user,
            message_type=message_type,
            context=context
        )

        sender.send()
