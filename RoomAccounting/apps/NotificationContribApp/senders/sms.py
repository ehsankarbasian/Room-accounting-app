from apps.NotificationApp.registry import SenderRegistry
from apps.NotificationApp.interfaces import MessageSenderInterface

from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(SenderType.SMS)
class SmsSender(MessageSenderInterface):
    pass
