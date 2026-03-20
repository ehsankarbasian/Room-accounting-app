from apps.NotificationApp.core.types import UserProtocol
from enum import Enum

from .message_factory import MessageFactory


class NotificationDispatcher:
    
    @staticmethod
    def send(user: UserProtocol, message_type: Enum, context: dict):
        
        sender = MessageFactory.get_sender(
            user=user,
            message_type=message_type,
            context=context
        )

        sender.send()
