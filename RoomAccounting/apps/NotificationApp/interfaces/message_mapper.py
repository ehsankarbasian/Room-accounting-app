from abc import ABC, abstractmethod

from .canonical import CanonicalMessageInterface


class MessageMapperInterface(ABC):

    @staticmethod
    @abstractmethod
    def map(data) -> CanonicalMessageInterface:
        pass
