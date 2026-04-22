
class ChannelResolverError(Exception):
    """Base exception for the notification framework channel resolver"""
    pass


class ChannelOverrideConflictError(ChannelResolverError):
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


class ChannelUnavailableError(ChannelResolverError):
    """Requested channel is not available for the recipient."""

    def __init__(self, channel_type):
        self.channel_type = channel_type

        super().__init__(
            "Requested notification channel is unavailable: "
            f"recipient has no verified '{channel_type}' channel configured."
        )


class NoAvailableChannelError(ChannelResolverError):
    """Recipient has no verified notification channels."""

    def __init__(self, recipient):
        self.recipient = recipient

        super().__init__(
            "Notification delivery failed: "
            f"recipient '{recipient}' does not have any verified notification channels configured."
        )


class NoPreferredChannelAvailableError(ChannelResolverError):
    """None of the preferred channels are available."""

    def __init__(self, preferred):
        self.preferred = preferred

        super().__init__(
            "None of the preferred notification channels are available: "
            f"preferred={preferred}. "
            "The recipient either does not have these channels configured or they are not verified."
        )
