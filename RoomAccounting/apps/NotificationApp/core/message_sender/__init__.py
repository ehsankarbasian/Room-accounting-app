from .concrete.email import EmailSender
from .concrete.sms import SmsSender
from .concrete.terminal import TerminalSender


SENDER_MAP = {
    "email": EmailSender,
    "sms": SmsSender,
    "terminal": TerminalSender,
}


__all__ = ["SENDER_MAP"]
