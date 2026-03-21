from apps.NotificationApp.core.registry import MapperRegistry

from apps.NotificationContribApp.core.interfaces import MessageMapperInterface
from apps.NotificationContribApp.core.models.canonical import NotificationCanonicalMessage, Button
from apps.NotificationContribApp.notification_types import MessageType

from .data_model import OtpDataModel


@MapperRegistry.register(name=MessageType.OTP)
class OtpMessageMapper(MessageMapperInterface):

    @staticmethod
    def map(data: OtpDataModel) -> NotificationCanonicalMessage:
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

        message = NotificationCanonicalMessage(
            text=text,
            buttons=buttons
        )

        return message
