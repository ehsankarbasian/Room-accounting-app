from ..interface.sender_interface import MessageSenderInterface
from apps.NotificationApp.core.registry import SenderRegistry


@SenderRegistry.register(name="sms")
class SmsSender(MessageSenderInterface):
    pass
