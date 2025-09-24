from abc import ABC, abstractmethod


class DraftInterface(ABC):
    
    @abstractmethod
    def build(self, context: dict) -> str:
        pass
