from ...interfaces import PermissionInterface, MessageSenderInterface
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
    def has_permission(recipient, *, channel: MessageSenderInterface):
        
        this_recipient_channels = NotificationChannel.objects.for_recipient(recipient)
        the_specific_channel = this_recipient_channels.filter(id=channel.id)
        channel_is_verified = the_specific_channel.filter(is_verified=True).exists()
        
        return channel_is_verified


class NotVerified(PermissionInterface):

    @staticmethod
    def has_permission(recipient, *, channel: MessageSenderInterface):
        return not Verified.has_permission(recipient, channel=channel)
