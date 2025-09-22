from .message_sender.email import EmailSender
from .message_sender.sms import SmsSender

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import User
    from apps.NotificationApp.models import NotificationMethod
    from .message_sender.interface import MessageSenderInterface


SENDER_MAP = {
    "email": EmailSender,
    "sms": SmsSender,
}


class MessageFactory:
    
    @staticmethod
    def get_sender(user: User,
                   message_type: str,
                   context: dict
                   ) -> MessageSenderInterface:
        # method: NotificationMethod = user.notification_methods.get(is_primary=True)
        method: NotificationMethod = user.notification_methods.get()
        context["identifier"] = method.identifier
        
        SenderClass = SENDER_MAP[method.method_type]
        sender: MessageSenderInterface = SenderClass(message_type=message_type,
                                                     context=context)
        
        return sender
