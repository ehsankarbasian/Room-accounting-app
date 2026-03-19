from .registry import make_registry as _make_registry

from apps.NotificationApp.core.interfaces import (
    MessageSenderInterface,
    MessageBuilderInterface
)


# Create separate registries for different domains
BUILDER_REGISTRY, register_builder = _make_registry(interface=MessageBuilderInterface)
SENDER_REGISTRY, register_sender = _make_registry(interface=MessageSenderInterface)


class BuilderRegistry:
    REGISTRY = BUILDER_REGISTRY
    register = register_builder

class SenderRegistry:
    REGISTRY = SENDER_REGISTRY
    register = register_sender
