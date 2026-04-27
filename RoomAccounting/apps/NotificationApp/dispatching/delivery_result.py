from dataclasses import dataclass, field
from typing import Optional, Type, List


@dataclass
class AttemptTrace:
    sender_class: Type
    channel_type: Optional[str]
    identifier: Optional[str]
    attempt_number: int
    success: bool
    error: Optional[Exception]
    duration_ms: int


@dataclass
class DeliveryStatus:
    success: bool
    message_class: Type
    sender_class: Optional[Type]
    channel_type: Optional[str]
    identifier: Optional[str]
    attempts: int
    last_exception: Optional[Exception]
    fallback_used: bool

    attempt_history: List[AttemptTrace] = field(default_factory=list)
    errors: List[Exception] = field(default_factory=list)
