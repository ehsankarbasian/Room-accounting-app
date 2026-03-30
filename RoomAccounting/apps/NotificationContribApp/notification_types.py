from enum import StrEnum


class SenderType(StrEnum):
    """
    Built-in sender types supported by contrib app.
    """

    EMAIL = "email"
    SMS = "sms"
    TERMINAL = "terminal"
    BALE = "bale"


class MessageType(StrEnum):
    """
    Built-in message types used by contrib services.
    """

    OTP = "otp"
    RESET_PASSWORD = "reset_password"
    VERIFY_CHANNEL = "verify_channel"
