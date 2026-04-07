from dataclasses import dataclass

from ....interfaces.message_base import MessageDefinitionInterface
from ....interfaces.message_mapper import MessageMapperInterface


#################################### Canonical message utils ####################################

from dataclasses import dataclass
from typing import List, Optional

from ....interfaces.message_mapper import CanonicalMessageInterface


@dataclass
class Button:
    """
    Interactive button that may appear in supported channels
    """

    text: str
    target: str


@dataclass
class CanonicalMessage(CanonicalMessageInterface):
    """
    Canonical message representation used internally by the notification framework.

    All message definitions are mapped into this format before
    being rendered by specific senders.
    """

    text: str
    buttons: Optional[List[Button]] = None


#################################### Message class ####################################

from ....contrib.permissions import NotVerified


class VerifyChannelMessage(MessageDefinitionInterface):

    permission_classes = (NotVerified, )

    @dataclass
    class Data:
        verification_url: str

    
    class Mapper(MessageMapperInterface):

        @staticmethod
        def map(data: "VerifyChannelMessage.Data") -> CanonicalMessage:
            text=f"Please verify your channel by visiting this link:\n{data.verification_url}"
            return CanonicalMessage(text=text)
