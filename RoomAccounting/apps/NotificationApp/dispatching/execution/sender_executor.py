"""
SenderExecutor is responsible for performing the actual delivery attempt loop
for sender classes, including retries, timeout handling, and attempt tracing.
"""

import time
from concurrent.futures import TimeoutError as FuturesTimeoutError

from ..context import SenderDispatchContext
from ..delivery_result import AttemptTrace, DeliveryStatus

from ..pipeline.resolvers import ChannelResolver, ChannelSelectionOptions
from ..pipeline.permissions import ensure_permissions
from ..pipeline.timeout import execute_with_timeout
from ..errors import MessagePermissionDeniedError


class SenderExecutor:
    """Executes delivery attempts for sender chains within the notification pipeline."""

    @staticmethod
    def execute_chain(
        sender_chain,
        recipient,
        message_class,
        canonical_message,
        channel_selection_options,
        attempts,
        timeout_seconds,
        primary_resolved_channel,
    ):

        errors = []

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
                SenderExecutor._execute_sender(context)

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

        return DeliveryStatus(
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


    @staticmethod
    def _execute_sender(context: SenderDispatchContext) -> None:
        """
        Perform the delivery execution flow for a single sender, including
        permission check, retry loop, timeout handling, and trace recording.
        """

        resolved_channel = ChannelResolver.resolve(
            recipient=context.recipient,
            options=ChannelSelectionOptions(
                channel_override=context.sender_class,
                require_verified=context.channel_selection_options.require_verified,
            ),
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
                    context.timeout_seconds,
                )

                SenderExecutor._record_attempt(
                    context=context,
                    attempt_number=attempt_number,
                    start_time=start_time,
                    success=True,
                    error=None,
                )

                context.success = True
                context.last_exception = None
                return

            except FuturesTimeoutError:
                error = TimeoutError(
                    f"Sender execution exceeded timeout of {context.timeout_seconds} seconds"
                )

                SenderExecutor._record_attempt(
                    context=context,
                    attempt_number=attempt_number,
                    start_time=start_time,
                    success=False,
                    error=error,
                )

                context.last_exception = error

            except Exception as new_exception:
                SenderExecutor._record_attempt(
                    context=context,
                    attempt_number=attempt_number,
                    start_time=start_time,
                    success=False,
                    error=new_exception,
                )

                context.last_exception = new_exception

        context.success = False


    # Internal utility for tracing attempts
    @staticmethod
    def _record_attempt(
        context: SenderDispatchContext,
        attempt_number: int,
        start_time: float,
        success: bool,
        error: Exception | None,
    ) -> None:
        duration = int((time.monotonic() - start_time) * 1000)

        context.attempt_history.append(
            AttemptTrace(
                sender_class=context.sender_class,
                channel_type=context.channel_type,
                identifier=context.identifier,
                attempt_number=attempt_number,
                success=success,
                error=error,
                duration_ms=duration,
            )
        )
