"""
Each message definition can declare a set of permission classes using:
    permission_classes = (...)
"""

from abc import ABC, abstractmethod


class PermissionInterface(ABC):
    
    @staticmethod
    @abstractmethod
    def has_permission(user) -> bool:
        pass
