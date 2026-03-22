from dataclasses import dataclass
from typing import Optional

from apps.NotificationApp.registry import MessageRegistry
from apps.NotificationApp.interfaces.message_base import MessageDefinitionInterface

from apps.NotificationContribApp.notification_types import MessageType
from apps.NotificationApp.interfaces.message_mapper import MessageMapperInterface
from apps.NotificationContribApp.messages.canonical import CanonicalMessage


@MessageRegistry.register(MessageType.RESET_PASSWORD)
class ResetPasswordMessage(MessageDefinitionInterface):

    @dataclass
    class Data:
        reset_token: str
        username: Optional[str] = None


    class Mapper(MessageMapperInterface):

        @staticmethod
        def map(data: "ResetPasswordMessage.Data") -> CanonicalMessage:
            result = f"{data.username} TOKEN: {data.reset_token}"
            return CanonicalMessage(text=result)
