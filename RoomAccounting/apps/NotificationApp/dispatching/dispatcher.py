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

from enum import Enum
from typing import Type, Optional, List

from ..registry import MessageRegistry, SenderRegistry
from ..interfaces import MessageDefinitionInterface

from .resolver import ChannelResolver
from .errors import MessagePermissionDenied


class NotificationDispatcher:

    # TODO(v2): Introduce a NotificationOptions object to support advanced dispatch controls
    # such as async, timeout, scheduling, retries, and channel fallback.
    @staticmethod
    def send(
        recipient,
        message_type: Enum,
        data: Type,
        *,
        channel_override: Optional[Enum] = None,
        preferred_channels: Optional[List[Enum]] = None
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
                If message_type or data are invalid.
            KeyError
                If the message or sender has not been registered.
        """

        if not isinstance(message_type, Enum):
            raise TypeError(
                f"'message_type' must be an Enum instance, not {type(message_type).__name__}"
            )

        if not is_dataclass(data):
            raise TypeError(
                f"data must be a dataclass instance, got {type(data).__name__}"
            )

        message_definition: MessageDefinitionInterface = MessageRegistry.get(message_type)
        expected_data_model = message_definition.Data

        if not isinstance(data, expected_data_model):
            raise TypeError(
                f"{message_type} expects {expected_data_model.__name__} instance, "
                f"got {type(data).__name__}"
            )

        notification_channel = ChannelResolver.resolve(
            recipient=recipient,
            channel_override=channel_override,
            preferred_channels=preferred_channels
        )

        for permission in message_definition.permission_classes:
            
            if not permission.has_permission(recipient):
                
                raise MessagePermissionDenied(
                    message_type=message_definition,
                    permission_class=permission
                )
        
        sender_class = SenderRegistry.get(notification_channel.channel_type)
        identifier = notification_channel.identifier

        mapper_class = message_definition.Mapper
        canonical_message = mapper_class.map(data=data)

        sender_class.send(
            identifier=identifier,
            message=canonical_message,
        )
