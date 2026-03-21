from .registry import make_registry as _make_registry

from apps.NotificationApp.core.interfaces import MessageSenderInterface
from apps.NotificationContribApp.core.interfaces import MessageMapperInterface


# Create separate registries for different domains
SENDER_REGISTRY, register_sender = _make_registry(interface=MessageSenderInterface)
DATAMODEL_REGISTRY, register_datamodel = _make_registry(interface=None)
MAPPER_REGISTRY, register_mapper = _make_registry(interface=MessageMapperInterface)
MESSAGE_REGISTRY, register_message = _make_registry(interface=None)


class SenderRegistry:
    REGISTRY = SENDER_REGISTRY
    register = register_sender

class DataModelRegistry:
    REGISTRY = DATAMODEL_REGISTRY
    register = register_datamodel

class MapperRegistry:
    REGISTRY = MAPPER_REGISTRY
    register = register_mapper

class MessageRegistry:
    REGISTRY = MESSAGE_REGISTRY
    register = register_message
