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

import time
from concurrent.futures import TimeoutError as FuturesTimeoutError
from dataclasses import dataclass, field
from typing import Optional, Type, List

from ..registry.message_options import MessageOptionsRegistry
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
class AttemptTrace:
    attempt_number: int
    success: bool
    error: Optional[Exception]
    duration_ms: int


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

    attempt_history: List[AttemptTrace] = field(default_factory=list)


@dataclass
class DeliveryStatus:
    success: bool
    message_class: Type
    sender_class: Optional[Type]
    channel_type: Optional[str]
    identifier: Optional[str]
    attempts: int
    last_exception: Optional[Exception]
    fallback_used: bool

    attempt_history: List[AttemptTrace] = field(default_factory=list)
    errors: List[Exception] = field(default_factory=list)


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

        errors: List[Exception] = []

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
                    return DeliveryStatus(
                        success=True,
                        message_class=message_class,
                        sender_class=sender_class,
                        channel_type=context.channel_type,
                        identifier=context.identifier,
                        attempts=len(context.attempt_history),
                        last_exception=None,
                        fallback_used=(sender_class != sender_chain[0]),
                        attempt_history=context.attempt_history,
                        errors=errors
                    )

                last_exception = context.last_exception
                last_channel_type = context.channel_type
                last_identifier = context.identifier

                errors.append(context.last_exception)

            except MessagePermissionDeniedError as permission_exception:
                errors.append(permission_exception)
                last_exception = permission_exception
                continue

        retry_exception_object = MaxRetryExceededError(
            attempts=attempts,
            last_exception=last_exception,
            channel=last_channel_type,
            identifier=last_identifier
        )

        retry_exception_object.delivery_status = DeliveryStatus(
            success=False,
            message_class=message_class,
            sender_class=None,
            channel_type=last_channel_type,
            identifier=last_identifier,
            attempts=attempts,
            last_exception=last_exception,
            fallback_used=len(sender_chain) > 1,
            errors=errors
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

        for attempt_number in range(1, context.attempts + 1):

            start_time = time.monotonic()

            try:
                execute_with_timeout(
                    context.sender_class,
                    context.identifier,
                    context.canonical_message,
                    context.timeout_seconds
                )

                duration = int((time.monotonic() - start_time) * 1000)

                context.attempt_history.append(
                    AttemptTrace(
                        attempt_number=attempt_number,
                        success=True,
                        error=None,
                        duration_ms=duration
                    )
                )

                context.success = True
                context.last_exception = None
                return

            except FuturesTimeoutError:

                duration = int((time.monotonic() - start_time) * 1000)

                error = TimeoutError(
                    f"Sender execution exceeded timeout of {context.timeout_seconds} seconds"
                )

                context.attempt_history.append(
                    AttemptTrace(
                        attempt_number=attempt_number,
                        success=False,
                        error=error,
                        duration_ms=duration
                    )
                )

                context.last_exception = error

            except Exception as new_exception:

                duration = int((time.monotonic() - start_time) * 1000)

                context.attempt_history.append(
                    AttemptTrace(
                        attempt_number=attempt_number,
                        success=False,
                        error=new_exception,
                        duration_ms=duration
                    )
                )

                context.last_exception = new_exception

        context.success = False
