from apps.NotificationApp.core.message_types.interface.draft_interface import DraftInterface

from apps.NotificationApp.core.registry import PayloadRegistry


@PayloadRegistry.register(name="otp")
class OtpDraft(DraftInterface):
    
    @staticmethod
    def build(context):
        final_text = f'Final payload text: {context}'
        print(final_text)
        return final_text
