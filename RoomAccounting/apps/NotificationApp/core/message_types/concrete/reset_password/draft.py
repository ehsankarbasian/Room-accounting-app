from ...interface.draft_interface import DraftInterface


class ResetPasswordDraft(DraftInterface):
    
    @staticmethod
    def build(context):
        final_text = context['token']
        return final_text
