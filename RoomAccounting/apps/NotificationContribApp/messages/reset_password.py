from dataclasses import dataclass
from typing import Optional

from apps.NotificationApp.registry import MessageRegistry
from apps.NotificationApp.interfaces.message_base import MessageDefinitionInterface
from apps.NotificationApp.interfaces.message_mapper import MessageMapperInterface

from apps.NotificationContribApp.notification_types import MessageType
from apps.NotificationContribApp.message_schema import CanonicalMessage


@MessageRegistry.register(MessageType.RESET_PASSWORD)
class ResetPasswordMessage(MessageDefinitionInterface):

    @dataclass
    class Data:
        reset_token: str
        username: Optional[str] = None


    class Mapper(MessageMapperInterface):
        """
        Maps ResetPasswordMessage.Data to CanonicalMessage.
        """

        @staticmethod
        def map(data: "ResetPasswordMessage.Data") -> CanonicalMessage:
            text = f"{data.username} TOKEN: {data.reset_token}"
            return CanonicalMessage(text=text)
