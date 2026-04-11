from dataclasses import dataclass, field
from typing import List

from ..interfaces import CanonicalMessageInterface

from .components import Button, ButtonLink


@dataclass
class CanonicalMessageBase(CanonicalMessageInterface):
    """
    Canonical message representation used internally by the notification framework.

    All message definitions are mapped into this format before
    being rendered by specific senders.
    """

    text: str
    
    buttons: List[Button] = field(default_factory=list)
    button_links: List[ButtonLink] = field(default_factory=list)
