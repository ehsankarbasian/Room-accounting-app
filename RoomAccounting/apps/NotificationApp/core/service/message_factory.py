from ..registry import SenderRegistry

from enum import Enum

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.NotificationApp.core.types import UserProtocol
    from apps.NotificationApp.models import NotificationMethod
    from apps.NotificationApp.core.interfaces.sender_interface import MessageSenderInterface


class MessageFactory:
    
    @staticmethod
    def get_sender(user: UserProtocol,
                   message_type: Enum,
                   context: dict
                ) -> MessageSenderInterface:
        
        if not isinstance(message_type, Enum):
            raise TypeError(
                f"'message_type' must be an Enum instance, not {type(message_type).__name__}"
            )
        
        method: NotificationMethod = NotificationMethod.objects.get(user=user, is_primary=True)
        
        context["identifier"] = method.identifier
        SenderClass = SenderRegistry.REGISTRY[method.method_type]
        sender: MessageSenderInterface = SenderClass(message_type=message_type,
                                                     context=context)
        
        return sender
