from abc import ABC, abstractmethod
from typing import Any

from .canonical import CanonicalMessageInterface


class MessageSenderInterface(ABC):
    """
    Sender interface for delivering notifications through specific channels.

    Each sender implementation is responsible for converting canonical
    messages into platform-specific payloads and delivering them.
    """

    @classmethod
    def send(cls, identifier: Any, message: CanonicalMessageInterface) -> None:
        """
        Execute the sender pipeline.

        identifier:
            Channel-specific recipient identifier
            (phone number, email, chat_id, etc).
        message:
            Canonical message object.
        """

        payload = cls.render_payload(message)
        cls.send_payload(identifier, payload)

    @staticmethod
    @abstractmethod
    def render_payload(message: CanonicalMessageInterface) -> Any:
        """
        Convert a canonical message into a channel-specific payload.
        """
        pass

    @staticmethod
    @abstractmethod
    def send_payload(identifier: Any, payload: Any) -> None:
        """
        Deliver the prepared payload to the destination channel.
        """
        pass
