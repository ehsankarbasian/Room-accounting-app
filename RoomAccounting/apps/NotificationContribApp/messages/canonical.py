from typing import List, Optional

from dataclasses import dataclass

from apps.NotificationApp.interfaces import CanonicalMessageInterface


# TODO: Create folder later (when extended message item)


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
