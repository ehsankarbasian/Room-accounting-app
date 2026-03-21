from enum import Enum

from typing import Type

from apps.NotificationApp.core.types import UserProtocol
from apps.NotificationApp.core.registry import MapperRegistry

from .message_factory import MessageFactory


class NotificationDispatcher:
    
    @staticmethod
    def send(user: UserProtocol, message_type: Enum, data: Type):
        
        if not isinstance(message_type, Enum):
            raise TypeError(
                f"'message_type' must be an Enum instance, not {type(message_type).__name__}"
            )
        
        sender = MessageFactory.get_sender(user=user)
        
        MapperClass = MapperRegistry.REGISTRY[message_type]
        cononical_data = MapperClass.map(data=data)
        
        sender.send(message=cononical_data)
