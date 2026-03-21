from apps.NotificationContribApp.core.interfaces import MessageMapperInterface
from apps.NotificationContribApp.core.models.canonical import NotificationCanonicalMessage

from .data_model import ResetPasswordDataModel

from apps.NotificationApp.core.registry import MapperRegistry
from apps.NotificationContribApp.notification_types import MessageType


@MapperRegistry.register(name=MessageType.RESET_PASSWORD)
class ResetPasswordMapper(MessageMapperInterface):

    @staticmethod
    def map(data: ResetPasswordDataModel) -> NotificationCanonicalMessage:

        result = f'{data.username} TOKEN: {data.reset_token}'
        return NotificationCanonicalMessage(text=result)
