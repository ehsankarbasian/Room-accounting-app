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


class IsOwner(AbstractPermissionMessage):

    @classmethod
    def has_permission(cls, request, view):
        user = request.user
        return (
            user.is_authenticated
            and getattr(user, "role", None) == "room_owner"
        )

    @classproperty
    def permission_denied_message(cls):
        return "Only room owners can access this resource"


class IsPerson(AbstractPermissionMessage):

    @classmethod
    def has_permission(cls, request, view):
        user = request.user
        return (
            user.is_authenticated
            and getattr(user, "role", None) == "person"
        )

    @classproperty
    def permission_denied_message(cls):
        return "Only persons can access this resource"

