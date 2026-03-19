from enum import StrEnum


class SenderType(StrEnum):
    EMAIL = "email"
    SMS = "sms"
    TERMINAL = "terminal"


class MessageType(StrEnum):
    OTP = "otp"
    RESET_PASSWORD = "reset_password"
