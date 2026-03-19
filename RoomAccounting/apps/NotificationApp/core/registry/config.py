from .registry import make_registry as _make_registry

from apps.NotificationApp.core.interfaces import (
    MessageSenderInterface,
    MessageBuilderInterface,
    DraftInterface
)


# Create separate registries for different domains
PAYLOAD_REGISTRY, register_payload = _make_registry(interface=DraftInterface)
BUILDER_REGISTRY, register_builder = _make_registry(interface=MessageBuilderInterface)
SENDER_REGISTRY, register_sender = _make_registry(interface=MessageSenderInterface)


class PayloadRegistry:
    REGISTRY = PAYLOAD_REGISTRY
    register = register_payload

class BuilderRegistry:
    REGISTRY = BUILDER_REGISTRY
    register = register_builder

class SenderRegistry:
    REGISTRY = SENDER_REGISTRY
    register = register_sender
