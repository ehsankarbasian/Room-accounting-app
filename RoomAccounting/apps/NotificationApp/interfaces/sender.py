from abc import ABC, abstractmethod
from typing import Any

from .canonical import CanonicalMessageInterface


class MessageSenderInterface(ABC):

    @classmethod
    def send(cls, identifier: Any, message: CanonicalMessageInterface) -> None:
        payload = cls.render_payload(message)
        cls.send_payload(identifier, payload)

    @staticmethod
    @abstractmethod
    def render_payload(message: CanonicalMessageInterface) -> Any:
        # Converts canonical CanonicalMessageInterface → platform specific payload (dict)
        pass
    
    @staticmethod
    @abstractmethod
    def send_payload(identifier: Any, payload: dict) -> None:
        # Renders payload accordint to specific message channel:
        pass
