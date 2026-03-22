from abc import ABC, abstractmethod
from typing import Any

from .canonical import CanonicalMessageInterface


class MessageMapperInterface(ABC):
    """
    Contract for mapping domain message data into canonical messages.
    
    Responsible for transforming domain-level message data into
    a canonical message representation.
    """

    @staticmethod
    @abstractmethod
    def map(data: Any) -> CanonicalMessageInterface:
        """
        Transform message data into a canonical message.
            - data: Instance of the message definition's Data model.
        """
        pass
