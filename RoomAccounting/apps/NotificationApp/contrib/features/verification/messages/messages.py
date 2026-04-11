from dataclasses import dataclass

from .....interfaces.message_base import MessageDefinitionInterface
from .....interfaces.message_mapper import MessageMapperInterface

from .....message_schema import CanonicalMessageBase
from .....message_schema.components import ButtonLink

from .....contrib.permissions import NotVerified


class VerifyChannelMessage(MessageDefinitionInterface):

    permission_classes = (NotVerified, )

    @dataclass
    class Data:
        verification_token: str
        verification_url: str

    
    class Mapper(MessageMapperInterface):

        @staticmethod
        def map(data: "VerifyChannelMessage.Data") -> CanonicalMessageBase:
            
            text = f"Please click on the button below to verify your channel identifier\nOr use the token *{data.verification_token.split('.')[1]}*"
            verify_channel_button = ButtonLink(
                text='Verify Channel Identifier',
                target=data.verification_url
            )
            
            return CanonicalMessageBase(text=text, button_links=[verify_channel_button])
