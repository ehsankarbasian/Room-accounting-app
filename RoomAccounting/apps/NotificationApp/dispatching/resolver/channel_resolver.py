from typing import Optional

from ...models import NotificationChannel

from .errors import (
    ChannelUnavailableError,
    NoAvailableChannelError,
    NoPreferredChannelAvailableError,
    ChannelOverrideConflictError,
)
from ...dispatch_options.channel_selection import ChannelSelectionOptions


class ChannelResolver:
    """
    Selection is based on:
        - verified recipient channels
        - optional channel override
        - optional preferred channel list

    Channels are deterministically ordered by:
        primary flag → priority → id.
    """

    @staticmethod
    def resolve(
        recipient,
        *,
        options: Optional[ChannelSelectionOptions] = ChannelSelectionOptions,
    ):
        """
        Select the best notification channel for the given recipient.

        Args:
            recipient: Target recipient instance.
            options: Options about how to resolve channel

        Returns:
            NotificationChannel: The selected channel instance.

        Raises:
            ChannelOverrideConflictError
            ChannelUnavailableError
            NoPreferredChannelAvailableError
            NoAvailableChannelError
        """

        # ------------------------------------------------
        # 1. VALIDATION (guard clauses)
        # ------------------------------------------------

        # Prevent inconsistent configuration where override
        # is not included in the preferred channel list.
        if (
            options.channel_override
            and options.preferred_channels
            and options.channel_override not in options.preferred_channels
        ):
            raise ChannelOverrideConflictError(
                override=options.channel_override,
                preferred=options.preferred_channels
            )

        # ------------------------------------------------
        # 2. DATABASE QUERY (minimal, efficient)
        # ------------------------------------------------
        
        if options.explicit_channel:
            return options.explicit_channel

        # Base queryset: only verified channels for the recipient
        queryset = NotificationChannel.objects.for_recipient(recipient).filter(is_verified=options.require_verified)

        # Restrict to the explicitly requested channel
        if options.channel_override:
            queryset = queryset.filter(channel_type=options.channel_override.sender_key)

        # Restrict to preferred channel types
        if options.preferred_channels:
            queryset = queryset.filter(channel_type__in=options.preferred_channels)

        # Deterministic ordering for consistent selection
        channels = list(
            queryset.order_by(
                "-is_primary",
                "priority",
                "id",
            )
        )

        # ------------------------------------------------
        # 3. ERROR HANDLING + SELECTION
        # ------------------------------------------------

        if not channels:

            # Explicit channel requested but unavailable
            if options.channel_override:
                raise ChannelUnavailableError(options.channel_override.sender_key)

            # Preferred channels specified but none available
            if options.preferred_channels:
                raise NoPreferredChannelAvailableError(
                    preferred=options.preferred_channels
                )

            # Recipient has no verified channels
            raise NoAvailableChannelError(recipient)

        # First result is the selected channel due to ordering
        return channels[0]
