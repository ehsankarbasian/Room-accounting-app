from dataclasses import dataclass
from typing import Optional

from NotificationApp.registry import MessageRegistry
from NotificationApp.interfaces.message_base import MessageDefinitionInterface
from NotificationApp.interfaces.message_mapper import MessageMapperInterface

from ..notification_types import MessageType
from ..message_schema import CanonicalMessage


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
