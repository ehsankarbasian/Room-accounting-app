from abc import ABC, abstractmethod

from django.core.exceptions import PermissionDenied as _DefaultPermissionDenied
from django.utils.functional import classproperty


class _AbstractBasePermission(ABC):
    
    @classmethod
    @abstractmethod
    def has_permission(request, view):
        pass


class AbstractPermissionException(_AbstractBasePermission):
    permission_denied_exception = _DefaultPermissionDenied


class AbstractPermissionMessage(_AbstractBasePermission):
    
    @classproperty
    @abstractmethod
    def permission_denied_message(self):
        pass
