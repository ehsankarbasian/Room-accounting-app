from apps.NotificationApp.core.registry import SenderRegistry
from apps.NotificationApp.core.interfaces import MessageSenderInterface

from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(SenderType.SMS)
class SmsSender(MessageSenderInterface):
    pass
