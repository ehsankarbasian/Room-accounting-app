from apps.NotificationApp.core.registry import SenderRegistry

from apps.NotificationApp.core.interfaces.sender_interface import MessageSenderInterface


@SenderRegistry.register(name="sms")
class SmsSender(MessageSenderInterface):
    pass
