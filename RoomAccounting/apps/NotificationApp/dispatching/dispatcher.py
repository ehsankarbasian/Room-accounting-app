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

from typing import Type, Optional

from ..registry import SenderRegistry
from ..interfaces import MessageDefinitionInterface

from .options import DeliveryOptions
from .resolver import ChannelResolver, ChannelSelectionOptions
from .errors import MessagePermissionDenied


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
                
                raise MessagePermissionDenied(
                    message_class=message_class,
                    permission_class=permission
                )
        
        sender_class = SenderRegistry.get(notification_channel.channel_type)
        identifier = notification_channel.identifier

        mapper_class = message_class.Mapper
        canonical_message = mapper_class.map(data=data)

        attempts = max(1, delivery_options.retry_count + 1)
        timeout_seconds = delivery_options.timeout_seconds

        last_exception = None

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

        raise last_exception
