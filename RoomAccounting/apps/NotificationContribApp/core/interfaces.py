from abc import ABC, abstractmethod

from .models.canonical import NotificationCanonicalMessage


class MessageMapperInterface(ABC):

    @staticmethod
    @abstractmethod
    def map(data) -> NotificationCanonicalMessage:
        pass
