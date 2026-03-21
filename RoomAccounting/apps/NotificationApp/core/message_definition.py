from abc import ABC, abstractmethod


class MessageDefinition(ABC):
    
    Data: type
    Mapper: type
