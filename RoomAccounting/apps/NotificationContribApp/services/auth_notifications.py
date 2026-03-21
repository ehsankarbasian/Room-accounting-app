from apps.NotificationApp.core.service import NotificationDispatcher

from apps.NotificationContribApp.notification_types import MessageType
# from apps.NotificationContribApp.core.message_types.otp.data_model import OtpDataModel
from apps.NotificationContribApp.core.messages.otp import OtpMessage

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import User, Person


class AuthNotifications:
    
    @staticmethod
    def send_otp(user: User, code: str):
        data = OtpMessage.Data(code=code)
        NotificationDispatcher.send(user, MessageType.OTP, data)
    
    @staticmethod
    def send_message_identifier_verification(user: User):
        pass
    
    @staticmethod
    def send_person_message_identifier_verification(person: Person):
        pass
