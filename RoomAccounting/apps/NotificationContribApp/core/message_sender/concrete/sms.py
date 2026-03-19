from apps.NotificationApp.core.registry import SenderRegistry

from apps.NotificationApp.core.message_sender.interface.sender_interface import MessageSenderInterface


@SenderRegistry.register(name="sms")
class SmsSender(MessageSenderInterface):
    pass
