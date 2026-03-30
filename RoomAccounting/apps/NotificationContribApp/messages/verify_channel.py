from dataclasses import dataclass

from apps.NotificationApp.registry import MessageRegistry
from apps.NotificationApp.interfaces.message_base import MessageDefinitionInterface
from apps.NotificationApp.interfaces.message_mapper import MessageMapperInterface

from apps.NotificationContribApp.notification_types import MessageType
from apps.NotificationContribApp.message_schema import CanonicalMessage
from apps.NotificationContribApp.permissions import NotVerified


@MessageRegistry.register(MessageType.VERIFY_CHANNEL)
class VerifyChannelMessage(MessageDefinitionInterface):

    permission_classes = (NotVerified, )

    @dataclass
    class Data:
        verification_url: str

    
    class Mapper(MessageMapperInterface):

        @staticmethod
        def map(data: "VerifyChannelMessage.Data") -> CanonicalMessage:
            text=f"Please verify your channel by visiting this link:\n{data.verification_url}",
            return CanonicalMessage(text=text)
