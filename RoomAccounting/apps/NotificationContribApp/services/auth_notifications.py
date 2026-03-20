from apps.NotificationApp.core.service import MessageFactory

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import User, Person


class AuthNotifications:
    
    @staticmethod
    def send_otp(user: User, code: str):
        context = {'code': code}
        sender = MessageFactory.get_sender(user, "otp", context)
        sender.send()
    
    @staticmethod
    def send_message_identifier_verification(user: User):
        pass
    
    @staticmethod
    def send_person_message_identifier_verification(person: Person):
        pass
