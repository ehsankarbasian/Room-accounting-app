from dataclasses import dataclass

from ......interfaces.message_base import MessageDefinitionInterface
from ......interfaces.message_mapper import MessageMapperInterface

from ......message_schema import CanonicalMessageBase
from ......message_schema.components import ButtonLink

from .....permissions import Verified


class ForgotPasswordMessage(MessageDefinitionInterface):
    
    permission_classes = (Verified, )

    @dataclass
    class Data:
        code: str
        reset_password_url: str


    class Mapper(MessageMapperInterface):

        @staticmethod
        def map(data: "ForgotPasswordMessage.Data") -> CanonicalMessageBase:

            text = f"Reset your password using the link below\ncode: *{data.code}*"
            
            reset_password_button = ButtonLink(
                text='Reset Password',
                target=f"{data.reset_password_url}"
            )
            
            return CanonicalMessageBase(text=text, button_links=[reset_password_button])
