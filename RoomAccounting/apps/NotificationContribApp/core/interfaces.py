from abc import ABC, abstractmethod
from .models.canonical import NotificationMessage


class MessageMapperInterface(ABC):

    @abstractmethod
    def map(self, data) -> NotificationMessage:
        pass
