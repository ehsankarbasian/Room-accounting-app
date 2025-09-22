from abc import ABC, abstractmethod


class MessageSenderInterface(ABC):
    
    @abstractmethod
    def __init__(self, message_type, context):
        pass
    
    @abstractmethod
    def build_payload(self):
        pass
    
    @property
    @abstractmethod
    def payload(self):
        pass
    
    @abstractmethod
    def send(self):
        pass
