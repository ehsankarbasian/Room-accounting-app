from dataclasses import dataclass
from typing import Optional

from apps.NotificationApp.interfaces.message_base import MessageDefinitionInterface
from apps.NotificationApp.interfaces.message_mapper import MessageMapperInterface
from apps.NotificationApp.contrib.permissions import Verified

from apps.NotificationContribApp.message_schema import CanonicalMessage
from apps.NotificationContribApp.permissions import NotLoggedIn


class ResetPasswordMessage(MessageDefinitionInterface):
    
    permission_classes = (NotLoggedIn, Verified)

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
