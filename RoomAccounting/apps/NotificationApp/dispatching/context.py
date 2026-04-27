from dataclasses import dataclass, field
from typing import Optional, Type, List

from ..interfaces import MessageDefinitionInterface

from .options import ChannelSelectionOptions
from .delivery_result import AttemptTrace


@dataclass
class SenderDispatchContext:
    sender_class: Type
    recipient: object
    message_class: Type[MessageDefinitionInterface]
    canonical_message: object
    channel_selection_options: ChannelSelectionOptions
    attempts: int
    timeout_seconds: int

    resolved_channel: Optional[object] = None
    channel_type: Optional[str] = None
    identifier: Optional[str] = None
    last_exception: Optional[Exception] = None
    success: bool = False

    attempt_history: List[AttemptTrace] = field(default_factory=list)
