from apps.NotificationApp.core.interfaces import MessageBuilderInterface
from apps.NotificationApp.core.registry import BuilderRegistry

from apps.NotificationContribApp.notification_types import MessageType

from .draft import OtpDraft
from .data_model import OtpDataModel


@BuilderRegistry.register(name=MessageType.OTP)
class OtpBuilder(MessageBuilderInterface):
    
    draft_class = OtpDraft
    
    def build_message(self, data: OtpDataModel):
        return f"Your temp code is {data.code}"
