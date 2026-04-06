from typing import Optional, List
from enum import Enum

from ..models import NotificationChannel

from .errors import (
    ChannelUnavailableError,
    NoAvailableChannelError,
    NoPreferredChannelAvailableError,
    ChannelOverrideConflictError,
)


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
        channel_override: Optional[Enum] = None,
        preferred_channels: Optional[List[Enum]] = None,
        is_verified = True
    ):
        """
        Select the best notification channel for the given recipient.

        Args:
            recipient: Target recipient instance.
            channel_override: Explicit channel type requested by the caller.
            preferred_channels: Ordered list of acceptable channel types.

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
            channel_override
            and preferred_channels
            and channel_override not in preferred_channels
        ):
            raise ChannelOverrideConflictError(
                override=channel_override,
                preferred=preferred_channels
            )

        # ------------------------------------------------
        # 2. DATABASE QUERY (minimal, efficient)
        # ------------------------------------------------

        # Base queryset: only verified channels for the recipient
        queryset = NotificationChannel.objects.for_recipient(recipient).filter(is_verified=is_verified)

        # Restrict to the explicitly requested channel
        if channel_override:
            queryset = queryset.filter(channel_type=channel_override)

        # Restrict to preferred channel types
        if preferred_channels:
            queryset = queryset.filter(channel_type__in=preferred_channels)

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
            if channel_override:
                raise ChannelUnavailableError(channel_override)

            # Preferred channels specified but none available
            if preferred_channels:
                raise NoPreferredChannelAvailableError(
                    preferred=preferred_channels
                )

            # Recipient has no verified channels
            raise NoAvailableChannelError(recipient)

        # First result is the selected channel due to ordering
        return channels[0]
