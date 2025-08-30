from abc import ABC, abstractmethod

from django.core.exceptions import PermissionDenied


class AbstractPermission(ABC):
    permission_denied_exception = PermissionDenied
    
    @classmethod
    @abstractmethod
    def has_permission(self, request, view):
        pass
    
    @property
    @abstractmethod
    def permission_denied_message(self):
        pass
