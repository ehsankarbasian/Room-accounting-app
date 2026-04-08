from dataclasses import dataclass

from apps.NotificationApp.contrib.message_schema import CanonicalMessageBase


@dataclass
class CanonicalMessage(CanonicalMessageBase):
    """
    Canonical message representation used internally by the notification framework.

    All message definitions are mapped into this format before
    being rendered by specific senders.
    """
