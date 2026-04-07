"""
Each message definition can declare a set of permission classes using:
    permission_classes = (...)
"""

from typing import Any, Optional
from abc import ABC, abstractmethod

from .sender import MessageSenderInterface


class PermissionInterface(ABC):
    
    @staticmethod
    @abstractmethod
    def has_permission(recipient: Any, *, channel: Optional[MessageSenderInterface]) -> bool:
        pass
