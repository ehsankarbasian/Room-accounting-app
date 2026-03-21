from dataclasses import dataclass
from typing import Optional

from apps.NotificationApp.core.registry import MessageRegistry
from apps.NotificationApp.core.message_definition import MessageDefinitionInterface

from apps.NotificationContribApp.notification_types import MessageType
from apps.NotificationContribApp.core.interfaces import MessageMapperInterface
from apps.NotificationContribApp.core.models.canonical import NotificationCanonicalMessage


@MessageRegistry.register(MessageType.RESET_PASSWORD)
class ResetPasswordMessage(MessageDefinitionInterface):

    @dataclass
    class Data:
        reset_token: str
        username: Optional[str] = None


    class Mapper(MessageMapperInterface):

        @staticmethod
        def map(data: "ResetPasswordMessage.Data") -> NotificationCanonicalMessage:
            result = f"{data.username} TOKEN: {data.reset_token}"
            return NotificationCanonicalMessage(text=result)
