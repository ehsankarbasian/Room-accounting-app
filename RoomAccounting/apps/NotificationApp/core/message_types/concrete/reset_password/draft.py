from ...interface.draft_interface import DraftInterface
from .data_model import MessageContext


class ResetPasswordDraft(DraftInterface):
    
    @staticmethod
    def build(context: MessageContext):
        final_text = context['token']
        return final_text
