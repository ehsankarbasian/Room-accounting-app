from enum import StrEnum


class SenderType(StrEnum):
    """
    Built-in sender types supported by contrib app.
    """

    EMAIL = "email"
    SMS = "sms"
    TERMINAL = "terminal"
    BALE = "bale"
