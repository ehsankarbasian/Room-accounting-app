from typing import Optional, List
from enum import Enum

from ..models import NotificationChannel

from .errors import (
    ChannelUnavailableError,
    NoAvailableChannelError,
    NoPreferredChannelAvailableError,
)


class ChannelResolver:

    @staticmethod
    def resolve(
        user,
        *,
        channel_override: Optional[Enum] = None,
        preferred_channels: Optional[List[Enum]] = None
    ):
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
