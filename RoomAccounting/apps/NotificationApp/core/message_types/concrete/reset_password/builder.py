from ...interface.builder_interface import MessageBuilderInterface
from .payload import ResetPasswordPayload


from django.template.loader import get_template


class ResetPasswordBuilder(MessageBuilderInterface):
    
    def build_message(self, context: dict):
        payload = ResetPasswordPayload.build(context)
        
        email = context['identifier']
        context = {
            'email': email,
            'name': "__TODO__",
            'token': payload}
        
        html_content = get_template('AuthApp/reset_password.html').render(context=context)
        return html_content
