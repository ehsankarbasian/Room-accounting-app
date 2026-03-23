from ..models import NotificationChannel

from .errors import (
    ChannelUnavailableError,
    NoAvailableChannelError,
)


class ChannelResolver:

    @staticmethod
    def resolve(user, channel_override=None):

        queryset = NotificationChannel.objects.filter(
            user=user,
            is_verified=True,
        )

        if channel_override:
            queryset = queryset.filter(channel_type=channel_override)

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

            raise NoAvailableChannelError(user)

        return channels[0]
