from ..registry import SenderRegistry

from enum import Enum

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.NotificationApp.core.types import UserProtocol
    from apps.NotificationApp.models import NotificationMethod
    from apps.NotificationApp.core.interfaces.sender_interface import MessageSenderInterface

from apps.NotificationContribApp.core.models.canonical import NotificationCanonicalMessage


class MessageFactory:
    
    @staticmethod
    def get_sender(user: UserProtocol) -> MessageSenderInterface:
        
        method: NotificationMethod = NotificationMethod.objects.get(user=user, is_primary=True)
        
        SenderClass = SenderRegistry.REGISTRY[method.method_type]
        sender: MessageSenderInterface = SenderClass(identifier=method.identifier)
        
        return sender
