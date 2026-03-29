from abc import ABC, abstractmethod


class PermissionInterface(ABC):
    
    @staticmethod
    @abstractmethod
    def has_permission(user):
        pass
