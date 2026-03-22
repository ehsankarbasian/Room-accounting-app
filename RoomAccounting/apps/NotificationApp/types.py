"""
Type-level contracts shared across the notification framework.
"""

from typing import Protocol


class UserProtocol(Protocol):
    """
    Minimal user contract required by the dispatcher.

    Any user object used with the notification system must expose:
        - id: unique integer identifier
    """
    
    id: int
