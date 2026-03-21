from dataclasses import dataclass

from apps.NotificationApp.core.registry import DataModelRegistry
from apps.NotificationContribApp.notification_types import MessageType


@DataModelRegistry.register(MessageType.OTP)
@dataclass
class OtpDataModel:
    code: str
