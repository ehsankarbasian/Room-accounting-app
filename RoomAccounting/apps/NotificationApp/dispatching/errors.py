class NotificationError(Exception):
    """Base exception for the notification framework."""
    pass


class ChannelOverrideConflictError(NotificationError):
    """
    Raised when channel_override is not part of preferred_channels.
    """

    def __init__(self, override, preferred):
        self.override = override
        self.preferred = preferred

        super().__init__(
            "Invalid channel selection configuration: "
            f"channel_override '{override}' is not included in preferred_channels {preferred}. "
            "When both parameters are provided, the override channel must be part of the preferred list."
        )


class ChannelUnavailableError(NotificationError):
    """Requested channel is not available for the user."""

    def __init__(self, channel_type):
        self.channel_type = channel_type

        super().__init__(
            "Requested notification channel is unavailable: "
            f"user has no verified '{channel_type}' channel configured."
        )


class NoAvailableChannelError(NotificationError):
    """User has no verified notification channels."""

    def __init__(self, user):
        self.user = user

        super().__init__(
            "Notification delivery failed: "
            f"user '{user}' does not have any verified notification channels configured."
        )


class NoPreferredChannelAvailableError(NotificationError):
    """None of the preferred channels are available."""

    def __init__(self, preferred):
        self.preferred = preferred

        super().__init__(
            "None of the preferred notification channels are available: "
            f"preferred={preferred}. "
            "The user either does not have these channels configured or they are not verified."
        )
