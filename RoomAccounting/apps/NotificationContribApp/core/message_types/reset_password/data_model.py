from dataclasses import dataclass
from typing import Optional


@dataclass
class ResetPasswordDataModel:
    recipient: str
    reset_token: str
    username: Optional[str] = None
