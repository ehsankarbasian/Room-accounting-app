from .draft import ResetPasswordDraft
from .data_model import MessageContext

from django.template.loader import get_template

from apps.NotificationApp.core.message_types.interface.builder_interface import MessageBuilderInterface
from apps.NotificationApp.core.registry import BuilderRegistry


@BuilderRegistry.register(name="reset_password")
class ResetPasswordBuilder(MessageBuilderInterface):
    
    def build_message(self, context: MessageContext):
        payload = ResetPasswordDraft.build(context)
        
        email = context['identifier']
        context = {
            'email': email,
            'name': "__TODO__",
            'token': payload}
        
        html_content = get_template('AuthApp/reset_password.html').render(context=context)
        return html_content
