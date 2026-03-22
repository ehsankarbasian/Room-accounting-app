"""
NotificationDispatcher orchestrates the full notification delivery pipeline.

Pipeline:
    MessageDefinition.Data  →  MessageMapper  →  CanonicalMessage  →  Sender

Responsibilities:
    - Validate message type and data model
    - Resolve user's primary notification method (or overridden channel)
    - Transform message data into canonical representation
    - Delegate delivery to the appropriate sender
"""

from enum import Enum
from dataclasses import is_dataclass
from typing import Type

from apps.NotificationApp.types import UserProtocol
from apps.NotificationApp.registry import MessageRegistry, SenderRegistry
from apps.NotificationApp.models import NotificationChannel


class NotificationDispatcher:

    # TODO(v2): Introduce a NotificationOptions object to support advanced dispatch controls
    # such as priority, timeout, scheduling, retries, and channel fallback.
    @staticmethod
    def send(
        user: UserProtocol,
        message_type: Enum,
        data: Type,
        *,
        channel_override: Enum | None = None,
    ):
        """
        Execute the notification delivery pipeline.

        data:
            Dataclass instance matching the expected Data model of the message definition.

        channel_override:
            Optional override for the notification channel. If provided,
            the dispatcher will bypass the user's primary notification method.

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

        message_definition = MessageRegistry.get(message_type)
        expected_data_model = message_definition.Data

        if not isinstance(data, expected_data_model):
            raise TypeError(
                f"{message_type} expects {expected_data_model.__name__} instance, "
                f"got {type(data).__name__}"
            )

        # channel resolution
        if channel_override is None:
            notification_method = NotificationChannel.objects.get(
                user=user,
                is_primary=True,
            )
            sender_type = notification_method.channel_type

        else:
            sender_type = channel_override
            notification_method = NotificationChannel.objects.get(
                user=user,
                channel_type=channel_override,
            )
        
        sender_class = SenderRegistry.get(sender_type)

        mapper_class = message_definition.Mapper
        canonical_message = mapper_class.map(data=data)

        identifier = notification_method.identifier

        sender_class.send(
            identifier=identifier,
            message=canonical_message,
        )
