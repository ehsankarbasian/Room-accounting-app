from .concrete.email import EmailSender
from .concrete.sms import SmsSender


SENDER_MAP = {
    "email": EmailSender,
    "sms": SmsSender,
}


__all__ = ["SENDER_MAP"]
