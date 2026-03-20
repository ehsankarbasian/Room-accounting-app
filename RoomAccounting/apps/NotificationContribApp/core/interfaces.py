from abc import ABC, abstractmethod
from .models.canonical import NotificationCanonicalMessage


class MessageMapperInterface(ABC):

    @abstractmethod
    def map(self, data) -> NotificationCanonicalMessage:
        pass
