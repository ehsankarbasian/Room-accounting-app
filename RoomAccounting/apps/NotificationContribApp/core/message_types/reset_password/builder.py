from .draft import ResetPasswordDraft
from .data_model import MessageContext

from django.template.loader import get_template

from apps.NotificationApp.core.interfaces import MessageBuilderInterface
from apps.NotificationApp.core.registry import BuilderRegistry

from apps.NotificationContribApp.notification_types import MessageType


@BuilderRegistry.register(name=MessageType.RESET_PASSWORD)
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
