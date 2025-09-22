from .message_factory import MessageFactory

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import User


class NotificationFacade:
    
    @staticmethod
    def send_otp(user, code: str):
        context = {'code': code}
        sender = MessageFactory.get_sender(user, "otp", context)
        sender.send()
