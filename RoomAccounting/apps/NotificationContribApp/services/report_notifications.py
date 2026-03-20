from apps.NotificationApp.core.service import NotificationDispatcher

from apps.NotificationContribApp.notification_types import MessageType

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import Person


class ReportNotifications:
    
    @staticmethod
    def send_spend_report(person: Person):
        pass
    
    @staticmethod
    def send_transaction_report(person: Person):
        pass
    
    @staticmethod
    def send_final_report(person: Person):
        pass
