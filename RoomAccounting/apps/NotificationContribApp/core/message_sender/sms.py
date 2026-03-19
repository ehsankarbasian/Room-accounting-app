from apps.NotificationApp.core.registry import SenderRegistry

from apps.NotificationApp.core.interfaces import MessageSenderInterface


@SenderRegistry.register(name="sms")
class SmsSender(MessageSenderInterface):
    pass
