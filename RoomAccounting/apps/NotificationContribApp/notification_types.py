from enum import StrEnum


class SenderType(StrEnum):
    EMAIL = "email"
    SMS = "sms"
    TERMINAL = "terminal"
    BALE = "bale"


class MessageType(StrEnum):
    OTP = "otp"
    RESET_PASSWORD = "reset_password"
