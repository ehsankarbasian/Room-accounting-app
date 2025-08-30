from abc import ABC, abstractmethod

from django.core.exceptions import PermissionDenied as _DefaultPermissionDenied


class _AbstractBasePermission(ABC):
    
    @classmethod
    @abstractmethod
    def has_permission(request, view):
        pass


class AbstractPermissionException(_AbstractBasePermission):
    permission_denied_exception = _DefaultPermissionDenied


class AbstractPermissionMessage(_AbstractBasePermission):
    
    @property
    @abstractmethod
    def permission_denied_message(self):
        pass
