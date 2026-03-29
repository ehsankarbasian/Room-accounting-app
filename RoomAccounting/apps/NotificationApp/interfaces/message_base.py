from abc import ABC
from typing import Type, Iterable

from .permission import PermissionInterface
from .message_mapper import MessageMapperInterface


class MessageDefinitionInterface(ABC):
    """
    Each message type in the system must provide:
        - a Data model (dataclass)
        - a Mapper that converts Data to CanonicalMessage

    A message definition describes how a domain message is represented
    and transformed into a canonical notification message.
    """
    
    permission_classes: Iterable[Type[PermissionInterface]]

    Data: Type
    Mapper: Type[MessageMapperInterface]
