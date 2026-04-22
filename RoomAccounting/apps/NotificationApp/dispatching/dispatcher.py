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

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError

from typing import Type, List

from ..registry import SenderRegistry, MessageOptionsRegistry
from ..interfaces import MessageDefinitionInterface, MessageSenderInterface

from .resolver import ChannelResolver, ChannelSelectionOptions

from .errors import (
    MessagePermissionDeniedError,
    MaxRetryExceededError,
)


class NotificationDispatcher:

    # TODO(v2): Introduce a NotificationOptions object to support advanced dispatch controls
    # such as async, timeout, scheduling, and channel fallback.
    
    @staticmethod
    def send(
        recipient,
        message_class: Type[MessageDefinitionInterface],
        data: Type,
    ):
        """
        Execute the notification delivery pipeline.

        data:
            Dataclass instance matching the expected Data model of the message definition.

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

        config = MessageOptionsRegistry.get(message_class)
        delivery_options = config.delivery_options
        channel_selection_options = config.channel_selection_options

        primary_resolved_channel = ChannelResolver.resolve(
            recipient=recipient,
            options=channel_selection_options
        )

        mapper_class = message_class.Mapper
        canonical_message = mapper_class.map(data=data)

        attempts = max(1, delivery_options.retry_count + 1)
        timeout_seconds = delivery_options.timeout_seconds

        # Build the primary delivery channel based on the recipient's resolved notification method
        sender_classes: List[type[MessageSenderInterface]] = []
        primary_sender_class = SenderRegistry.get(primary_resolved_channel.channel_type)
        sender_classes.append(primary_sender_class)

        # Append fallback sender classes provided by delivery options for alternative delivery paths
        fallback_channels: List[type[MessageSenderInterface]] = []
        if delivery_options.fallback_channels:
            fallback_channels = delivery_options.fallback_channels
        sender_classes.extend(fallback_channels)

        last_exception = None
        last_channel_type = primary_resolved_channel.channel_type
        last_identifier = primary_resolved_channel.identifier

        for sender_class in sender_classes:

            resolved_channel = ChannelResolver.resolve(
                recipient=recipient,
                options=ChannelSelectionOptions(
                    channel_override=sender_class,
                    require_verified=channel_selection_options.require_verified
                )
            )

            identifier = resolved_channel.identifier
            channel_type = resolved_channel.channel_type

            try:
                for permission in message_class.permission_classes:
                    if not permission.has_permission(recipient, channel=resolved_channel):
                        raise MessagePermissionDeniedError(
                            message_class=message_class,
                            permission_class=permission
                        )

            except MessagePermissionDeniedError as permission_exception:
                last_exception = permission_exception
                last_channel_type = channel_type
                last_identifier = identifier
                continue

            for _ in range(attempts):
                try:
                    if timeout_seconds is not None:
                        
                        with ThreadPoolExecutor(max_workers=1) as executor:
                            
                            future = executor.submit(
                                sender_class.send,
                                identifier=identifier,
                                message=canonical_message,
                            )
                            future.result(timeout=timeout_seconds)
                            
                    else:
                        sender_class.send(
                            identifier=identifier,
                            message=canonical_message,
                        )

                    return

                except FuturesTimeoutError:
                    
                    last_exception = TimeoutError(
                        f"Sender execution exceeded timeout of {timeout_seconds} seconds"
                    )

                except Exception as new_exception:
                    last_exception = new_exception

            last_channel_type = channel_type
            last_identifier = identifier

        retry_exception_object = MaxRetryExceededError(
            attempts=attempts,
            last_exception=last_exception,
            channel=last_channel_type,
            identifier=last_identifier
        )
        raise retry_exception_object from last_exception
