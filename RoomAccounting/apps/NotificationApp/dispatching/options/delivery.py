from dataclasses import dataclass, fields
from typing import Optional, List, Any, Dict

from ...interfaces import MessageSenderInterface


@dataclass(frozen=True)
class DeliveryOptions:
    retry_count: int = 0
    timeout_seconds: Optional[float] = None
    fallback_channels: Optional[List[type[MessageSenderInterface]]] = None

    def copy_with(self, **overrides: Dict[str, Any]):
        valid_fields = {f.name for f in fields(self)}
        filtered = {k: v for k, v in overrides.items() if k in valid_fields}
        return DeliveryOptions(**{**self.__dict__, **filtered})
