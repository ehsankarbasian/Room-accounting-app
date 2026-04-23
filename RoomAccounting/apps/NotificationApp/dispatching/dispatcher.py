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
from dataclasses import dataclass
from typing import Optional, Type

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


@dataclass
class SenderDispatchContext:
    sender_class: Type
    recipient: object
    message_class: Type[MessageDefinitionInterface]
    canonical_message: object
    channel_selection_options: ChannelSelectionOptions
    attempts: int
    timeout_seconds: int

    resolved_channel: Optional[object] = None
    channel_type: Optional[str] = None
    identifier: Optional[str] = None
    last_exception: Optional[Exception] = None
    success: bool = False


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

        sender_chain = build_sender_chain(
            delivery_options,
            primary_resolved_channel
        )

        last_exception = None
        last_channel_type = primary_resolved_channel.channel_type
        last_identifier = primary_resolved_channel.identifier

        for sender_class in sender_chain:

            context = SenderDispatchContext(
                sender_class=sender_class,
                recipient=recipient,
                message_class=message_class,
                canonical_message=canonical_message,
                channel_selection_options=channel_selection_options,
                attempts=attempts,
                timeout_seconds=timeout_seconds,
            )

            try:
                NotificationDispatcher._dispatch_single_sender(context)

                if context.success:
                    return

                last_exception = context.last_exception
                last_channel_type = context.channel_type
                last_identifier = context.identifier

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
        context: SenderDispatchContext,
    ) -> None:

        resolved_channel = ChannelResolver.resolve(
            recipient=context.recipient,
            options=ChannelSelectionOptions(
                channel_override=context.sender_class,
                require_verified=context.channel_selection_options.require_verified
            )
        )

        context.resolved_channel = resolved_channel
        context.channel_type = resolved_channel.channel_type
        context.identifier = resolved_channel.identifier

        ensure_permissions(
            context.message_class,
            context.recipient,
            resolved_channel
        )

        for _ in range(context.attempts):
            try:
                execute_with_timeout(
                    context.sender_class,
                    context.identifier,
                    context.canonical_message,
                    context.timeout_seconds
                )

                context.success = True
                context.last_exception = None
                return

            except FuturesTimeoutError:
                context.last_exception = TimeoutError(
                    f"Sender execution exceeded timeout of {context.timeout_seconds} seconds"
                )

            except Exception as new_exception:
                context.last_exception = new_exception

        context.success = False
