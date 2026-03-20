from abc import ABC, abstractmethod
from typing import Any
from apps.NotificationContribApp.core.models.canonical import NotificationCanonicalMessage


class MessageSenderInterface(ABC):

    @abstractmethod
    def __init__(self, identifier: Any):
        # identifier = chat_id, phone_number, email, etc...
        self._identifier = identifier


    @abstractmethod
    def render_payload(self, message: NotificationCanonicalMessage) -> Any:
        # Converts canonical NotificationCanonicalMessage → platform specific payload (dict)
        pass


    @abstractmethod
    def send(self, payload: Any):
        # Sends payload to platform.
        pass
