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
        # return self.build_payload(message_type=message_type, context=context)
        pass
    
    @abstractmethod
    def send(self):
        pass
