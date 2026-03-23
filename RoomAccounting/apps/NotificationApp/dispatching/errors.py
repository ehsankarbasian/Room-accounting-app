
class NotificationError(Exception):
    """Base exception for notification framework."""
    pass


class ChannelUnavailableError(NotificationError):
    """Requested channel is not available for the user."""

    def __init__(self, channel_type):
        self.channel_type = channel_type
        super().__init__(
            f"No verified notification channel available for '{channel_type}'"
        )


class NoAvailableChannelError(NotificationError):
    """User has no verified notification channels."""

    def __init__(self, user):
        self.user = user
        super().__init__(
            f"User '{user}' has no verified notification channels"
        )


class NoPreferredChannelAvailableError(NotificationError):

    def __init__(self, preferred, actual):
        self.preferred = preferred
        self.actual = actual
        super().__init__(
            f"No channels match the preferred list {preferred}. "
            f"Available channels: {[c.channel_type for c in actual]}"
        )
