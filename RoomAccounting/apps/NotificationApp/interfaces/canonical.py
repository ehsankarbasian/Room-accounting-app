"""
A canonical message represents a normalized notification payload
independent of any delivery channel.
"""

from abc import ABC


class CanonicalMessageInterface(ABC):
    """
    Canonical messages act as an intermediate representation between
    domain-level message data and channel-specific payloads.
    """

    pass
