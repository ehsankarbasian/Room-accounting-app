from ...interface.payload_interface import PayloadInterface


class ResetPasswordPayload(PayloadInterface):
    
    @staticmethod
    def build(context):
        final_text = context['token']
        return final_text
