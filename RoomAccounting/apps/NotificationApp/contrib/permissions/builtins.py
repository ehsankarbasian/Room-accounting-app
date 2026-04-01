from ...interfaces import PermissionInterface
from ...models import NotificationChannel


class AllowAny(PermissionInterface):

    @staticmethod
    def has_permission(recipient):
        return True


class AllowNobody(PermissionInterface):

    @staticmethod
    def has_permission(recipient):
        return False


class Verified(PermissionInterface):

    @staticmethod
    def has_permission(recipient):
        return NotificationChannel.objects.for_recipient(recipient).filter(is_verified=True).exists()


class NotVerified(PermissionInterface):

    @staticmethod
    def has_permission(recipient):
        return not Verified.has_permission(recipient)
