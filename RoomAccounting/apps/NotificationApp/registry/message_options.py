from dataclasses import dataclass
from typing import Type, Dict

from ..interfaces import MessageDefinitionInterface
from ..dispatch_options import DeliveryOptions, ChannelSelectionOptions


@dataclass
class MessageDispatchConfig:
    delivery_options: DeliveryOptions
    channel_selection_options: ChannelSelectionOptions


class MessageOptionsRegistry:

    _registry: Dict[Type[MessageDefinitionInterface], MessageDispatchConfig] = {}

    _default_config = MessageDispatchConfig(
        delivery_options=DeliveryOptions(),
        channel_selection_options=ChannelSelectionOptions(),
    )

    @classmethod
    def set(
        cls,
        message_class: Type[MessageDefinitionInterface],
        *,
        delivery_options: DeliveryOptions = DeliveryOptions(),
        channel_selection_options: ChannelSelectionOptions = ChannelSelectionOptions(),
    ) -> None:

        if not issubclass(message_class, MessageDefinitionInterface):
            raise TypeError(
                "message_class must be a subclass of MessageDefinitionInterface"
            )

        cls._registry[message_class] = MessageDispatchConfig(
            delivery_options=delivery_options,
            channel_selection_options=channel_selection_options,
        )

    @classmethod
    def get(
        cls,
        message_class: Type[MessageDefinitionInterface],
    ) -> MessageDispatchConfig:

        if not issubclass(message_class, MessageDefinitionInterface):
            raise TypeError(
                "message_class must be a subclass of MessageDefinitionInterface"
            )

        return cls._registry.get(message_class, cls._default_config)
