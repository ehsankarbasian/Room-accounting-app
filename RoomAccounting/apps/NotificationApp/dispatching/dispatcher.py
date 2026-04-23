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

from concurrent.futures import TimeoutError as FuturesTimeoutError

from typing import Type

from ..registry import MessageOptionsRegistry
from ..interfaces import MessageDefinitionInterface

from .errors import (
    MessagePermissionDeniedError,
    MaxRetryExceededError,
)

from .pipeline.validators import ensure_valid_message_inputs
from .pipeline.resolvers import ChannelResolver, ChannelSelectionOptions
from .pipeline.resolvers import build_sender_chain
from .pipeline.permissions import ensure_permissions
from .pipeline.timeout import execute_with_timeout


class NotificationDispatcher:

    # TODO(v2): Introduce a NotificationOptions object to support advanced dispatch controls
    # such as async, scheduling, and etc.
    
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
        
        ensure_valid_message_inputs(message_class, data)

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

        sender_chain = build_sender_chain(delivery_options, primary_resolved_channel)

        last_exception = None
        last_channel_type = primary_resolved_channel.channel_type
        last_identifier = primary_resolved_channel.identifier

        for sender_class in sender_chain:
            
            try:
                success, exception, channel_type, identifier = (
                    NotificationDispatcher._dispatch_single_sender(
                        sender_class,
                        recipient,
                        canonical_message,
                        channel_selection_options,
                        attempts,
                        timeout_seconds,
                        message_class
                    )
                )

                if success:
                    return

                last_exception = exception
                last_channel_type = channel_type
                last_identifier = identifier

            except MessagePermissionDeniedError as permission_exception:
                last_exception = permission_exception
                continue

        retry_exception_object = MaxRetryExceededError(
            attempts=attempts,
            last_exception=last_exception,
            channel=last_channel_type,
            identifier=last_identifier
        )
        
        raise retry_exception_object from last_exception
    
    
    @staticmethod
    def _dispatch_single_sender(
        sender_class,
        recipient,
        canonical_message,
        channel_selection_options,
        attempts,
        timeout_seconds,
        message_class
    ):

        resolved_channel = ChannelResolver.resolve(
            recipient=recipient,
            options=ChannelSelectionOptions(
                channel_override=sender_class,
                require_verified=channel_selection_options.require_verified
            )
        )

        channel_type = resolved_channel.channel_type
        identifier = resolved_channel.identifier

        ensure_permissions(message_class, recipient, resolved_channel)

        last_exception = None

        for _ in range(attempts):
            try:
                execute_with_timeout(
                    sender_class,
                    identifier,
                    canonical_message,
                    timeout_seconds
                )
                return True, None, channel_type, identifier

            except FuturesTimeoutError:
                last_exception = TimeoutError(
                    f"Sender execution exceeded timeout of {timeout_seconds} seconds"
                )

            except Exception as new_exception:
                last_exception = new_exception

        return False, last_exception, channel_type, identifier
