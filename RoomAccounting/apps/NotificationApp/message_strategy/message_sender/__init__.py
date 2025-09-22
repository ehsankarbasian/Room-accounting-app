from .email import EmailSender
from .sms import SmsSender


SENDER_MAP = {
    "email": EmailSender,
    "sms": SmsSender,
}


__all__ = ["SENDER_MAP"]
