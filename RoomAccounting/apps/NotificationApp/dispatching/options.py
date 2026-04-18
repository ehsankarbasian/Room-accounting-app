from dataclasses import dataclass, fields
from typing import Optional, List, Any, Dict


@dataclass(frozen=True)
class NotificationOptions:
    retry_count: int = 0
    timeout_seconds: Optional[float] = None
    fallback_channels: Optional[List[Any]] = None
    channel_override: Optional[Any] = None
    preferred_channels: Optional[List[Any]] = None
    require_verified: bool = True

    def copy_with(self, **overrides: Dict[str, Any]):
        valid_fields = {f.name for f in fields(self)}
        filtered = {k: v for k, v in overrides.items() if k in valid_fields}
        return NotificationOptions(**{**self.__dict__, **filtered})
