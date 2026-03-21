from abc import ABC, abstractmethod
from typing import Any

from apps.NotificationContribApp.core.models.canonical import NotificationCanonicalMessage


class MessageSenderInterface(ABC):

    def __init__(self, identifier: Any):
        # identifier = chat_id, phone_number, email, etc...
        self.identifier = identifier

    def send(self, message: NotificationCanonicalMessage) -> None:
        payload = self.render_payload(message)
        self.send_payload(payload)

    @abstractmethod
    def render_payload(self, message: NotificationCanonicalMessage) -> Any:
        # Converts canonical NotificationCanonicalMessage → platform specific payload (dict)
        pass
    
    @abstractmethod
    def send_payload(self, payload: dict) -> None:
        # Renders payload accordint to specific message channel:
        pass
