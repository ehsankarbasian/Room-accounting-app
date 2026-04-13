from dataclasses import dataclass

from .....interfaces.message_base import MessageDefinitionInterface
from .....interfaces.message_mapper import MessageMapperInterface

from .....message_schema import CanonicalMessageBase

from ....permissions import Verified


class OtpMessage(MessageDefinitionInterface):
    
    permission_classes = (Verified, )

    @dataclass
    class Data:
        code: str


    class Mapper(MessageMapperInterface):
        """
        Converts OTP data into a CanonicalMessage representation.
        """

        @staticmethod
        def map(data: "OtpMessage.Data") -> CanonicalMessageBase:

            text = f"Your temporary code is:\n*{data.code}*"
            return CanonicalMessageBase(text=text)
