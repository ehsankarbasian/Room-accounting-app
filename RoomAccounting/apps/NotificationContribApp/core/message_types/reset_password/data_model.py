from typing import Optional

from dataclasses import dataclass

from apps.NotificationApp.core.registry import DataModelRegistry
from apps.NotificationContribApp.notification_types import MessageType


@DataModelRegistry.register(MessageType.RESET_PASSWORD)
@dataclass
class ResetPasswordDataModel:
    reset_token: str
    username: Optional[str] = None
