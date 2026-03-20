from enum import Enum

from apps.NotificationApp.core.types import UserProtocol

from .message_factory import MessageFactory


class NotificationDispatcher:
    
    @staticmethod
    def send(user: UserProtocol, message_type: Enum, context: dict):
        
        if not isinstance(message_type, Enum):
            raise TypeError(
                f"'message_type' must be an Enum instance, not {type(message_type).__name__}"
            )
        
        sender = MessageFactory.get_sender(
            user=user,
            message_type=message_type,
            context=context
        )

        sender.send()
