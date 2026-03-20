from .registry import make_registry as _make_registry

from apps.NotificationApp.core.interfaces import (
    MessageSenderInterface,
    MessageBuilderInterface
)


# Create separate registries for different domains
BUILDER_REGISTRY, register_builder = _make_registry(interface=MessageBuilderInterface) # TODO: delete
SENDER_REGISTRY, register_sender = _make_registry(interface=MessageSenderInterface)
DATAMODEL_REGISTRY, register_datamodel = _make_registry(interface=None)
MAPPER_REGISTRY, register_mapper = _make_registry(interface=None)


# TODO: delete
class BuilderRegistry:
    REGISTRY = BUILDER_REGISTRY
    register = register_builder

class SenderRegistry:
    REGISTRY = SENDER_REGISTRY
    register = register_sender

class DataModelRegistry:
    REGISTRY = DATAMODEL_REGISTRY
    register = register_datamodel

class MapperRegistry:
    REGISTRY = MAPPER_REGISTRY
    register = register_mapper
