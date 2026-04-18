from dataclasses import dataclass

from ......interfaces.message_base import MessageDefinitionInterface
from ......interfaces.message_mapper import MessageMapperInterface

from ......message_schema import CanonicalMessageBase
from ......message_schema.components import ButtonLink

from .....permissions import Verified


class OtpMessage(MessageDefinitionInterface):
    
    permission_classes = (Verified, )

    @dataclass
    class Data:
        code: str
        verify_otp_url: str


    class Mapper(MessageMapperInterface):
        """
        Converts OTP data into a CanonicalMessage representation.
        """

        @staticmethod
        def map(data: "OtpMessage.Data") -> CanonicalMessageBase:

            text = f"Your temporary code is:\n*{data.code}*"
            
            verify_button_link = ButtonLink(
                text="Verify OTP code",
                target=data.verify_otp_url
            )
            
            return CanonicalMessageBase(text=text, button_links=[verify_button_link])
