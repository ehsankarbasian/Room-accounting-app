from enum import Enum
from dataclasses import is_dataclass

from typing import Type

from apps.NotificationApp.core.types import UserProtocol
# from apps.NotificationApp.core.registry import MapperRegistry, DataModelRegistry
from apps.NotificationApp.core.registry import MessageRegistry

from .message_factory import MessageFactory


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

        # expected_datamodel = DataModelRegistry.REGISTRY[message_type]
        expected_datamodel = MessageRegistry.REGISTRY[message_type].Data
        if not isinstance(data, expected_datamodel):
            raise TypeError(
                f"{message_type} expects {expected_datamodel.__name__} instance, "
                f"got {type(data).__name__}"
            )

        # mapper = MapperRegistry.REGISTRY[message_type]
        mapper = MessageRegistry.REGISTRY[message_type].Mapper
        canonical_data = mapper.map(data=data)

        sender = MessageFactory.get_sender(user=user)
        sender.send(message=canonical_data)
