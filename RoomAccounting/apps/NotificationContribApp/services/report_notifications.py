from apps.NotificationApp.dispatching import NotificationDispatcher

from apps.NotificationContribApp.notification_types import MessageType

from typing import TYPE_CHECKING
if TYPE_CHECKING or True:
    from apps.ReportApp.models import Person


class ReportNotifications:
    """
    Notification service responsible for report-related messages.
    This layer orchestrates sending reports through the notification framework.
    """
    
    @staticmethod
    def send_spend_report(person: "Person"):
        pass
    
    @staticmethod
    def send_transaction_report(person: "Person"):
        pass
    
    @staticmethod
    def send_final_report(person: "Person"):
        pass
