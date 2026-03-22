from dataclasses import dataclass

from apps.NotificationApp.registry import MessageRegistry
from apps.NotificationApp.interfaces.message_base import MessageDefinitionInterface
from apps.NotificationApp.interfaces.message_mapper import MessageMapperInterface

from apps.NotificationContribApp.notification_types import MessageType
from apps.NotificationContribApp.messages.canonical import CanonicalMessage, Button


@MessageRegistry.register(MessageType.OTP)
class OtpMessage(MessageDefinitionInterface):

    @dataclass
    class Data:
        code: str


    class Mapper(MessageMapperInterface):

        @staticmethod
        def map(data: "OtpMessage.Data") -> CanonicalMessage:
            """
            Converts OtpDataModel into the canonical NotificationMessage.

            Business/UI logic such as constructing buttons,
            building template-like text, or preparing URLs lives here.
            """

            text = f"Your temporary login code is: {data.code}"
            otp_login_url = f"https://example.com/login?code={data.code}"

            buttons = [
                Button(
                    text="ورود یکبار مصرف",
                    target=otp_login_url
                )
            ]

            message = CanonicalMessage(
                text=text,
                buttons=buttons
            )

            return message
