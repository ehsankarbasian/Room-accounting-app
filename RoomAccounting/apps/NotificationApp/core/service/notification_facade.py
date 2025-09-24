from .message_factory import MessageFactory

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import User, Person


class NotificationFacade:
    
    @staticmethod
    def send_otp(user: User, code: str):
        context = {'code': code}
        sender = MessageFactory.get_sender(user, "otp", context)
        sender.send()
    
    @staticmethod
    def send_reset_password(user: User, email: str, token: str):
        context = {'token': token, 'identifier': email}
        sender = MessageFactory.get_sender(user, "reset_password", context)
        sender.send()
    
    @staticmethod
    def send_message_identifier_verification(user: User):
        pass
    
    @staticmethod
    def send_person_message_identifier_verification(person: Person):
        pass
    
    @staticmethod
    def send_spend_report(person: Person):
        pass
    
    @staticmethod
    def send_transaction_report(person: Person):
        pass
    
    @staticmethod
    def send_final_report(person: Person):
        pass
