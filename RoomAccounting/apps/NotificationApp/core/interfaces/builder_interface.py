from abc import ABC, abstractmethod

from .draft_interface import DraftInterface


class MessageBuilderInterface(ABC):
    
    # TODO: enforce
    draft_class: DraftInterface
    
    @abstractmethod
    def build_message(self, data: dict) -> dict | str:
        pass
