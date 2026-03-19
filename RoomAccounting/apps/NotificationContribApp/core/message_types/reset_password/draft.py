from apps.NotificationApp.core.message_types.interface.draft_interface import DraftInterface
from apps.NotificationApp.core.registry import PayloadRegistry

from .data_model import MessageContext


@PayloadRegistry.register(name="reset_password")
class ResetPasswordDraft(DraftInterface):
    
    @staticmethod
    def build(context: MessageContext):
        final_text = context['token']
        return final_text
