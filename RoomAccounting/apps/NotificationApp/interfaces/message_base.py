from abc import ABC

from .message_mapper import MessageMapperInterface


class MessageDefinitionInterface(ABC):
    
    Data: type
    Mapper: MessageMapperInterface
