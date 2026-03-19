from apps.NotificationApp.core.interfaces import DraftInterface
from apps.NotificationApp.core.registry import PayloadRegistry

from apps.NotificationContribApp.notification_types import MessageType

from .data_model import MessageContext


@PayloadRegistry.register(name=MessageType.RESET_PASSWORD)
class ResetPasswordDraft(DraftInterface):
    
    @staticmethod
    def build(context: MessageContext):
        final_text = context['token']
        return final_text
