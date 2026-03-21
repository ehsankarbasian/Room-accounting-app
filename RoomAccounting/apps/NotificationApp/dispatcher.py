from enum import Enum
from dataclasses import is_dataclass

from apps.NotificationApp.types import UserProtocol
from apps.NotificationApp.registry import MessageRegistry, SenderRegistry
from apps.NotificationApp.models import NotificationMethod

from typing import TYPE_CHECKING, Type
if TYPE_CHECKING or True:
    from apps.NotificationApp.types import UserProtocol


class NotificationDispatcher:
    
    @staticmethod
    def send(user: UserProtocol, message_type: Enum, data: Type):
        
        if not isinstance(message_type, Enum):
            raise TypeError(
                f"'message_type' must be an Enum instance, not {type(message_type).__name__}"
            )

        if not is_dataclass(data):
            raise TypeError(
                f"data must be a dataclass instance, got {type(data).__name__}"
            )

        expected_datamodel = MessageRegistry.REGISTRY[message_type].Data
        if not isinstance(data, expected_datamodel):
            raise TypeError(
                f"{message_type} expects {expected_datamodel.__name__} instance, "
                f"got {type(data).__name__}"
            )
        
        notification_method = NotificationMethod.objects.get(user=user, is_primary=True)
        sender_type = notification_method.method_type
        SenderClass = SenderRegistry.REGISTRY[sender_type]
        
        mapper = MessageRegistry.REGISTRY[message_type].Mapper
        canonical_data = mapper.map(data=data)
        identifier = notification_method.identifier
        
        SenderClass.send(identifier=identifier, message=canonical_data)
