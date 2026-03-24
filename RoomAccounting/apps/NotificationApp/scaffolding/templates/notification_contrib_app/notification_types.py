from enum import StrEnum


class SenderType(StrEnum):
    """
    Built-in sender types supported by contrib app.
    """

    EMAIL = "email"
    TERMINAL = "terminal"


class MessageType(StrEnum):
    """
    Built-in message types used by contrib services.
    """

    OTP = "otp"
    RESET_PASSWORD = "reset_password"
