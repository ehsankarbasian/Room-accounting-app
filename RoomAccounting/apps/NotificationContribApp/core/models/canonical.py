from typing import List, Optional

from dataclasses import dataclass


@dataclass
class Button:
    text: str
    target: str


@dataclass
class NotificationCanonicalMessage:
    text: str
    buttons: Optional[List[Button]] = None
