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

from typing import Type, List

from ..registry.message_options import MessageOptionsRegistry
from ..interfaces import MessageDefinitionInterface

from .errors import MessagePermissionDeniedError, MaxRetryExceededError

from .delivery_result import DeliveryStatus
from .context import SenderDispatchContext

from .pipeline.validators import ensure_valid_message_inputs
from .pipeline.resolvers import ChannelResolver
from .pipeline.resolvers import build_sender_chain

from .execution.sender_executor import SenderExecutor


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
                SenderExecutor.execute(context)

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
            fallback_used=(len(sender_chain) > 1),
            errors=errors
        )

        raise retry_exception_object from last_exception
