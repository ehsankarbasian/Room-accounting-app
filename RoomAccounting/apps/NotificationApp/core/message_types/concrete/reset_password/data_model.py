from dataclasses import dataclass
from typing import Optional


@dataclass
class MessageContext:
    recipient: str
    reset_token: str
    username: Optional[str] = None
