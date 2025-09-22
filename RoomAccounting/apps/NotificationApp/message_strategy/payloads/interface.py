from abc import ABC, abstractmethod


class PayloadInterface(ABC):
    
    @abstractmethod
    def build(self, context: dict):
        pass
