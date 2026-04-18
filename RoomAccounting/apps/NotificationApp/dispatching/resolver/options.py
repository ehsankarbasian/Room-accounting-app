from dataclasses import dataclass, fields
from typing import Optional, List, Any, Dict

from ...interfaces import MessageDefinitionInterface
from ...models import NotificationChannel


@dataclass(frozen=True)
class ChannelSelectionOptions:
    explicit_channel: Optional[NotificationChannel] = None
    channel_override: Optional[MessageDefinitionInterface] = None
    preferred_channels: Optional[List[MessageDefinitionInterface]] = None
    require_verified: bool = True

    def copy_with(self, **overrides: Dict[str, Any]):
        valid_fields = {f.name for f in fields(self)}
        filtered = {k: v for k, v in overrides.items() if k in valid_fields}
        return ChannelSelectionOptions(**{**self.__dict__, **filtered})
