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

from typing import Type

from ..registry.message_options import MessageOptionsRegistry
from ..interfaces import MessageDefinitionInterface

from .errors import MaxRetryExceededError

from .pipeline.validators import ensure_valid_message_inputs
from .pipeline.resolvers import resolve_channel, build_sender_chain

from .execution.sender_executor import SenderExecutor
from .delivery_result import DeliveryStatus

class NotificationDispatcher:

    # TODO(v2): Introduce a NotificationOptions object to support advanced dispatch controls
    # such as async, scheduling, and etc.

    @staticmethod
    def send(
        recipient,
        message_class: Type[MessageDefinitionInterface],
        data: Type,
    ) -> DeliveryStatus:
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

        primary_resolved_channel = resolve_channel(
            recipient=recipient,
            options=channel_selection_options
        )

        canonical_message = message_class.Mapper.map(data=data)

        attempts = max(1, delivery_options.retry_count + 1)
        timeout_seconds = delivery_options.timeout_seconds

        sender_chain = build_sender_chain(
            delivery_options,
            primary_resolved_channel
        )

        delivery_result = SenderExecutor.execute_chain(
            sender_chain=sender_chain,
            recipient=recipient,
            message_class=message_class,
            canonical_message=canonical_message,
            channel_selection_options=channel_selection_options,
            attempts=attempts,
            timeout_seconds=timeout_seconds,
            primary_resolved_channel=primary_resolved_channel,
        )

        if not delivery_result.success:

            retry_exception_object = MaxRetryExceededError(
                attempts=attempts,
                last_exception=delivery_result.last_exception,
                channel=delivery_result.channel_type,
                identifier=delivery_result.identifier
            )
            
            if (
                delivery_result.last_exception and
                delivery_result.last_exception not in delivery_result.errors
            ):
                delivery_result.errors.append(delivery_result.last_exception)

            delivery_result.last_exception = retry_exception_object

        return delivery_result
