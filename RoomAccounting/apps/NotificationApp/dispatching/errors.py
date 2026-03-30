class NotificationDispatchError(Exception):
    """Base exception for the notification framework."""
    pass


class ChannelOverrideConflictError(NotificationDispatchError):
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


class ChannelUnavailableError(NotificationDispatchError):
    """Requested channel is not available for the recipient."""

    def __init__(self, channel_type):
        self.channel_type = channel_type

        super().__init__(
            "Requested notification channel is unavailable: "
            f"recipient has no verified '{channel_type}' channel configured."
        )


class NoAvailableChannelError(NotificationDispatchError):
    """Recipient has no verified notification channels."""

    def __init__(self, recipient):
        self.recipient = recipient

        super().__init__(
            "Notification delivery failed: "
            f"recipient '{recipient}' does not have any verified notification channels configured."
        )


class NoPreferredChannelAvailableError(NotificationDispatchError):
    """None of the preferred channels are available."""

    def __init__(self, preferred):
        self.preferred = preferred

        super().__init__(
            "None of the preferred notification channels are available: "
            f"preferred={preferred}. "
            "The recipient either does not have these channels configured or they are not verified."
        )


class MessagePermissionDenied(NotificationDispatchError):
    """
    Raised when a notification message fails its permission checks.
    """

    def __init__(self, message_type, permission_class):
        super().__init__(
            f"Permission denied for message '{message_type.__name__}'. "
            f"Failed permission: '{permission_class.__name__}'."
        )
