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

from typing import Type, Optional, List

from ..registry import SenderRegistry
from ..interfaces import MessageDefinitionInterface, MessageSenderInterface

from .options import DeliveryOptions
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
        *,
        delivery_options: Optional[DeliveryOptions] = DeliveryOptions,
        channel_selection_options: Optional[ChannelSelectionOptions] = ChannelSelectionOptions,
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

        notification_channel = ChannelResolver.resolve(
            recipient=recipient,
            options=channel_selection_options
        )

        for permission in message_class.permission_classes:
            
            if not permission.has_permission(recipient, channel=notification_channel):
                
                raise MessagePermissionDeniedError(
                    message_class=message_class,
                    permission_class=permission
                )

        mapper_class = message_class.Mapper
        canonical_message = mapper_class.map(data=data)

        attempts = max(1, delivery_options.retry_count + 1)
        timeout_seconds = delivery_options.timeout_seconds

        # TODO: comment
        sender_classes: List[type[MessageSenderInterface]] = []
        primary_sender_class = SenderRegistry.get(notification_channel.channel_type)
        sender_classes.append(primary_sender_class)

        # TODO: comment
        fallback_channels: List[type[MessageSenderInterface]] = []
        if delivery_options.fallback_channels:
            fallback_channels = delivery_options.fallback_channels
        sender_classes.extend(fallback_channels)

        last_exception = None
        last_channel_type = notification_channel.channel_type
        last_identifier = notification_channel.identifier

        for sender_class in sender_classes:

            if sender_class is primary_sender_class:
                identifier = notification_channel.identifier
                channel_type = notification_channel.channel_type
            else:
                # TODO: use sender_class not the primary resolved channel
                identifier = notification_channel.identifier
                channel_type = sender_class.channel_type

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
