from abc import ABC, abstractmethod


class MessageBuilderInterface(ABC):
    
    @abstractmethod
    def build_message(self, context: dict) -> dict | str:
        pass
