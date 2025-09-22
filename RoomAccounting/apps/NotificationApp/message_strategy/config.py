from .message_sender import EmailSender, SmsSender
from .payloads import OtpPayload


SENDER_MAP = {
    "email": EmailSender,
    "sms": SmsSender,
}

PAYLOAD_MAP = {
    "otp": OtpPayload,
}
