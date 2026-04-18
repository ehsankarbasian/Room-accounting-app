
class NotificationDispatchError(Exception):
    """Base exception for the notification framework dispatcher"""
    pass


class MessagePermissionDenied(NotificationDispatchError):
    """
    Raised when a notification message fails its permission checks.
    """

    def __init__(self, message_class, permission_class):
        super().__init__(
            f"Permission denied for message '{message_class.__name__}'. "
            f"Failed permission: '{permission_class.__name__}'."
        )
