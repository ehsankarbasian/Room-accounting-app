from apps.NotificationApp.dispatcher import NotificationDispatcher

from apps.NotificationContribApp.notification_types import MessageType
from apps.NotificationContribApp.messages import OtpMessage

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING or True:
    from enum import Enum
    from apps.ReportApp.models import User, Person


class AuthNotifications:

    @staticmethod
    def send_otp(user: User, code: str, *, channel_name: Optional[Enum] = None):
        data = OtpMessage.Data(code=code)
        NotificationDispatcher.send(user, MessageType.OTP, data,
                                    channel_override=channel_name)
    
    @staticmethod
    def send_message_identifier_verification(user: User):
        pass
    
    @staticmethod
    def send_person_message_identifier_verification(person: Person):
        pass
