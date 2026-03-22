from typing import List, Optional

from dataclasses import dataclass

from apps.NotificationApp.interfaces import CanonicalMessageInterface


# TODO: Create folder later (when extended message item)


@dataclass
class Button:
    text: str
    target: str


@dataclass
class CanonicalMessage(CanonicalMessageInterface):
    text: str
    buttons: Optional[List[Button]] = None
