from typing import List, Optional
from dataclasses import dataclass

from apps.NotificationApp.interfaces import CanonicalMessageInterface

from .components import Button, ButtonLink


@dataclass
class CanonicalMessage(CanonicalMessageInterface):
    """
    Canonical message representation used internally by the notification framework.

    All message definitions are mapped into this format before
    being rendered by specific senders.
    """

    text: str
    
    buttons: Optional[List[Button]] = None
    button_links: Optional[List[ButtonLink]] = None
