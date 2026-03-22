from abc import ABC
from typing import Type

from .message_mapper import MessageMapperInterface


class MessageDefinitionInterface(ABC):
    """
    Each message type in the system must provide:
        - a Data model (dataclass)
        - a Mapper that converts Data to CanonicalMessage

    A message definition describes how a domain message is represented
    and transformed into a canonical notification message.
    """

    Data: Type
    Mapper: Type[MessageMapperInterface]
