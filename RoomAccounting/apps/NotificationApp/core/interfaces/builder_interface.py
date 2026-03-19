from abc import ABC, abstractmethod

from .draft_interface import DraftInterface


class MessageBuilderInterface(ABC):
    
    # TODO: enforce
    draft_class: DraftInterface
    
    @abstractmethod
    def build_message(self, context: dict) -> dict | str:
        pass
