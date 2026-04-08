from dataclasses import dataclass

from apps.NotificationApp.interfaces.message_base import MessageDefinitionInterface
from apps.NotificationApp.interfaces.message_mapper import MessageMapperInterface
from apps.NotificationApp.contrib.permissions import Verified

from apps.NotificationContribApp.message_schema import CanonicalMessage
from apps.NotificationApp.contrib.message_schema.components import Button
from apps.NotificationContribApp.permissions import NotLoggedIn


class OtpMessage(MessageDefinitionInterface):
    
    permission_classes = (NotLoggedIn, Verified)

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
