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

    @staticmethod
    def resolve(
        user,
        *,
        channel_override: Optional[Enum] = None,
        preferred_channels: Optional[List[Enum]] = None
    ):

        if (
            channel_override
            and preferred_channels
            and channel_override not in preferred_channels
        ):
            raise ChannelOverrideConflictError(
                channel_override,
                preferred_channels
            )

        queryset = NotificationChannel.objects.filter(
            user=user,
            is_verified=True,
        )

        if channel_override:
            queryset = queryset.filter(channel_type=channel_override)

        if preferred_channels:
            queryset = queryset.filter(channel_type__in=preferred_channels)

        channels = list(
            queryset.order_by(
                "-is_primary",
                "priority",
                "id",
            )
        )

        if not channels:

            if channel_override:
                raise ChannelUnavailableError(channel_override)

            if preferred_channels:
                raise NoPreferredChannelAvailableError(preferred_channels)

            raise NoAvailableChannelError(user)

        return channels[0]
