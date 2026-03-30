from NotificationApp.interfaces import PermissionInterface
from NotificationApp.models import NotificationChannel


class AllowAny(PermissionInterface):

    @staticmethod
    def has_permission(user):
        return True


class AllowNobody(PermissionInterface):

    @staticmethod
    def has_permission(user):
        return False


class Verified(PermissionInterface):

    @staticmethod
    def has_permission(user):
        return NotificationChannel.objects.filter(
            user=user,
            is_verified=True,
        ).exists()


class NotVerified(PermissionInterface):

    @staticmethod
    def has_permission(user):
        return not Verified.has_permission(user)


class LoggedIn(PermissionInterface):
    
    @staticmethod
    def has_permission(user):
        return user.is_authenticated


class NotLoggedIn(PermissionInterface):
    
    @staticmethod
    def has_permission(user):
        return not LoggedIn.has_permission(user)
