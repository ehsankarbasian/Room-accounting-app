from dataclasses import dataclass

from NotificationApp.registry import MessageRegistry
from NotificationApp.interfaces.message_base import MessageDefinitionInterface
from NotificationApp.interfaces.message_mapper import MessageMapperInterface

from ..notification_types import MessageType
from ..message_schema import CanonicalMessage
from ..message_schema.components import Button


@MessageRegistry.register(MessageType.OTP)
class OtpMessage(MessageDefinitionInterface):

    @dataclass
    class Data:
        code: str


    class Mapper(MessageMapperInterface):
        """
        Converts OTP data into a CanonicalMessage representation.
        """

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

            return CanonicalMessage(
                text=text,
                buttons=buttons
            )
