from apps.NotificationApp.core.interfaces import MessageBuilderInterface
from apps.NotificationApp.core.registry import BuilderRegistry

from apps.NotificationContribApp.notification_types import MessageType


@BuilderRegistry.register(name=MessageType.OTP)
class OTPBuilder(MessageBuilderInterface):
    
    def build_message(self, context: dict):
        text = f"Your temp code is {context['code']}"
        return text
