from .registry import make_registry as _make_registry

from apps.NotificationApp.core.interfaces import MessageSenderInterface
from apps.NotificationApp.core.message_definition import MessageDefinitionInterface


# Create separate registries for different domains
SENDER_REGISTRY, register_sender = _make_registry(interface=MessageSenderInterface)
MESSAGE_REGISTRY, register_message = _make_registry(interface=MessageDefinitionInterface)


class SenderRegistry:
    REGISTRY = SENDER_REGISTRY
    register = register_sender

class MessageRegistry:
    REGISTRY = MESSAGE_REGISTRY
    register = register_message
