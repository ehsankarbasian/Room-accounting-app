from ..registry import SenderRegistry


from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import User
    from apps.NotificationApp.models import NotificationMethod
    from ..message_sender.interface.sender_interface import MessageSenderInterface


class MessageFactory:
    
    @staticmethod
    def get_sender(user: User,
                   message_type: str,
                   context: dict
                   ) -> MessageSenderInterface:
        method: NotificationMethod = NotificationMethod.objects.get(user=user, is_primary=True)
        # context["identifier"] = method.identifier
        
        context["identifier"] = method.identifier
        SenderClass = SenderRegistry.REGISTRY[method.method_type]
        sender: MessageSenderInterface = SenderClass(message_type=message_type,
                                                     context=context)
        
        return sender
