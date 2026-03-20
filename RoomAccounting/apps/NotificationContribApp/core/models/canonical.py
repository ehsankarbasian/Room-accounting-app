from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Button:
    text: str
    target: str


@dataclass
class NotificationCanonicalMessage:
    text: str
    buttons: Optional[List[Button]] = None
