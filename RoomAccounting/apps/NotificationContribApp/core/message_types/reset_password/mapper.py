from django.template.loader import get_template

from apps.NotificationContribApp.core.interfaces import MessageMapperInterface
from apps.NotificationContribApp.core.models.canonical import NotificationCanonicalMessage

from .data_model import ResetPasswordDataModel

from apps.NotificationApp.core.registry import MapperRegistry
from apps.NotificationContribApp.notification_types import MessageType


@MapperRegistry.register(name=MessageType.RESET_PASSWORD)
class ResetPasswordMapper(MessageMapperInterface):

    @staticmethod
    def map(data: ResetPasswordDataModel) -> NotificationCanonicalMessage:

        context = {
            "email": data.recipient,
            "name": data.username or "",
            "token": data.reset_token,
        }

        html_content = get_template(
            "AuthApp/reset_password.html"
        ).render(context=context)

        return NotificationCanonicalMessage(
            text=html_content
        )
