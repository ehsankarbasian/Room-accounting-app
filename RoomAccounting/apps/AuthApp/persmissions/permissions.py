from django.utils.functional import classproperty

from apps.AuthApp.persmissions.abstract import AbstractPermissionMessage, AbstractPermissionException


class AllowAny(AbstractPermissionMessage):
    
    @classmethod
    def has_permission(self, request, view):
        return True
    
    @classproperty
    def permission_denied_message(self):
        return '__ALLOW_ANY__'


class IsAuthenticated(AbstractPermissionMessage):
    
    @classmethod
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    @classproperty
    def permission_denied_message(self):
        return 'Please sign in'


class IsAnonymous(AbstractPermissionMessage):
    
    @classmethod
    def has_permission(self, request, view):
        return request.user.is_anonymous
    
    @classproperty
    def permission_denied_message(self):
        return 'Please log out'
