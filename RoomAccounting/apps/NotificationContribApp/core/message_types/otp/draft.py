from apps.NotificationApp.core.interfaces import DraftInterface


class OtpDraft(DraftInterface):
    
    @staticmethod
    def build(context):
        final_text = f'Final payload text: {context}'
        print(final_text)
        return final_text
