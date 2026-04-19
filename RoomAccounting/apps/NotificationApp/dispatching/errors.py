
class NotificationDispatchError(Exception):
    """Base exception for the notification framework dispatcher"""
    pass


class MessagePermissionDeniedError(NotificationDispatchError):
    """
    Raised when a notification message fails its permission checks.
    """

    def __init__(self, message_class, permission_class):
        super().__init__(
            f"Permission denied for message '{message_class.__name__}'. "
            f"Failed permission: '{permission_class.__name__}'."
        )


class MaxRetryExceededError(NotificationDispatchError):
    """
    Raised when all retry attempts have been exhausted and the dispatcher
    could not successfully deliver the message.

    Attributes:
        attempts (int): Total number of attempts made.
        last_exception (Exception): The final exception thrown by the sender.
        channel (str): Channel type used for dispatch (e.g. "sms", "email").
        identifier (str): Target identifier used in the final send attempt.
    """

    def __init__(self, attempts, last_exception, channel, identifier):
        self.attempts = attempts
        self.last_exception = last_exception
        self.channel = channel
        self.identifier = identifier

        message = (
            f"Message delivery failed after {attempts} attempts using channel '{channel}' "
            f"with identifier '{identifier}'. Last error: {last_exception!r}"
        )

        super().__init__(message)
