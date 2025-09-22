from ..interface import PayloadInterface
from django.template.loader import render_to_string


class OtpPayload(PayloadInterface):
    
    @staticmethod
    def build(context):
        # html_body = render_to_string("emails/otp.html", context)
        final_text = f'Final payload text: {context}'
        print(final_text)
        return final_text
