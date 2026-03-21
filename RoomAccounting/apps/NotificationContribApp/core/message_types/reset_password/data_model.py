from dataclasses import dataclass
from typing import Optional


@dataclass
class ResetPasswordDataModel:
    reset_token: str
    username: Optional[str] = None
