"""
NotificationDispatcher orchestrates the full notification delivery pipeline.

Pipeline:
    MessageDefinition.Data  →  MessageMapper  →  CanonicalMessage  →  Sender

Responsibilities:
    - Validate message type and data model
    - Resolve user's primary notification method
    - Transform message data into canonical representation
    - Delegate delivery to the appropriate sender
"""

from enum import Enum
from dataclasses import is_dataclass
from typing import Type

from apps.NotificationApp.types import UserProtocol
from apps.NotificationApp.registry import MessageRegistry, SenderRegistry
from apps.NotificationApp.models import NotificationMethod


class NotificationDispatcher:

    @staticmethod
    def send(user: UserProtocol, message_type: Enum, data: Type):
        """
        Execute the notification delivery pipeline.

        data:
            Dataclass instance matching the expected Data model of the message definition.

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

        message_definition = MessageRegistry.REGISTRY[message_type]
        expected_data_model = message_definition.Data

        if not isinstance(data, expected_data_model):
            raise TypeError(
                f"{message_type} expects {expected_data_model.__name__} instance, "
                f"got {type(data).__name__}"
            )

        notification_method = NotificationMethod.objects.get(
            user=user,
            is_primary=True,
        )

        sender_type = notification_method.method_type
        sender_class = SenderRegistry.REGISTRY[sender_type]

        mapper_class = message_definition.Mapper
        canonical_message = mapper_class.map(data=data)

        identifier = notification_method.identifier

        sender_class.send(
            identifier=identifier,
            message=canonical_message,
        )
