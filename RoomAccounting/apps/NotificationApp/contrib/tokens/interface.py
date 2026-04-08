from abc import ABC, abstractmethod


class TokenGeneratorInterface(ABC):

    @staticmethod
    @abstractmethod
    def generate() -> str:
        pass
