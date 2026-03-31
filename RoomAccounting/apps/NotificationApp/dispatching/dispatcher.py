"""
NotificationDispatcher orchestrates the full notification delivery pipeline.

Pipeline:
    MessageDefinition.Data  →  MessageMapper  →  CanonicalMessage  →  Sender

Responsibilities:
    - Validate message type and data model
    - Resolve recipient's primary notification method (or overridden channel)
    - Transform message data into canonical representation
    - Delegate delivery to the appropriate sender
"""

from dataclasses import is_dataclass

from typing import Type, Optional, List

from ..registry import SenderRegistry
from ..interfaces import MessageDefinitionInterface

from .resolver import ChannelResolver
from .errors import MessagePermissionDenied


class NotificationDispatcher:

    # TODO(v2): Introduce a NotificationOptions object to support advanced dispatch controls
    # such as async, timeout, scheduling, retries, and channel fallback.
    @staticmethod
    def send(
        recipient,
        message_class: Type[MessageDefinitionInterface],
        data: Type,
        *,
        channel_override: Optional[MessageDefinitionInterface] = None,
        preferred_channels: Optional[List[MessageDefinitionInterface]] = None
    ):
        """
        Execute the notification delivery pipeline.

        data:
            Dataclass instance matching the expected Data model of the message definition.

        channel_override:
            Optional override for the notification channel. If provided,
            the dispatcher will bypass the recipient's primary notification method.

        Raises:
            TypeError
                If message_class or data are invalid.
            KeyError
                If the sender has not been registered.
        """

        if not issubclass(message_class, MessageDefinitionInterface):
            raise TypeError(
                f"'{message_class.__name__}' must be a MessageDefinitionInterface implementation"
            )

        if not is_dataclass(data):
            raise TypeError(
                f"data must be a dataclass instance, got {type(data).__name__}"
            )

        expected_data_model = message_class.Data

        if not isinstance(data, expected_data_model):
            raise TypeError(
                f"{message_class} expects {expected_data_model.__name__} instance, "
                f"got {type(data).__name__}"
            )

        notification_channel = ChannelResolver.resolve(
            recipient=recipient,
            channel_override=channel_override,
            preferred_channels=preferred_channels
        )

        for permission in message_class.permission_classes:
            
            if not permission.has_permission(recipient):
                
                raise MessagePermissionDenied(
                    message_class=message_class,
                    permission_class=permission
                )
        
        sender_class = SenderRegistry.get(notification_channel.channel_type)
        identifier = notification_channel.identifier

        mapper_class = message_class.Mapper
        canonical_message = mapper_class.map(data=data)

        sender_class.send(
            identifier=identifier,
            message=canonical_message,
        )
