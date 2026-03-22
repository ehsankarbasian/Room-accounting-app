"""
Central registry configuration for the notification framework.

SenderRegistry
    Maps notification method types to sender implementations.
MessageRegistry
    Maps message type enums to message definition implementations.
"""

from .registry import make_registry as _make_registry

from apps.NotificationApp.interfaces import (
    MessageSenderInterface,
    MessageDefinitionInterface,
)


# Create separate registries for different domains
_SENDER_REGISTRY, _register_sender = _make_registry(
    interface=MessageSenderInterface
)

_MESSAGE_REGISTRY, _register_message = _make_registry(
    interface=MessageDefinitionInterface
)


class _RegistryBase:
    """
    Base helper providing controlled access to registry dictionaries.

    This abstraction prevents external code from interacting directly
    with the internal dictionary structure.
    """

    _REGISTRY: dict

    @classmethod
    def get(cls, key):
        return cls._REGISTRY[key]


class SenderRegistry(_RegistryBase):
    _REGISTRY = _SENDER_REGISTRY
    register = _register_sender


class MessageRegistry(_RegistryBase):
    _REGISTRY = _MESSAGE_REGISTRY
    register = _register_message
