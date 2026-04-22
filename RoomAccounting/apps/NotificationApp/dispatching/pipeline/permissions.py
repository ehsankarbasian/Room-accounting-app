from ...interfaces import MessageDefinitionInterface
from ...models import NotificationChannel

from ..errors import MessagePermissionDeniedError


def ensure_permissions(
        message_class: MessageDefinitionInterface,
        recipient,
        resolved_channel: NotificationChannel,
    ):
    
    for permission in message_class.permission_classes:
        if not permission.has_permission(recipient, channel=resolved_channel):
            
            raise MessagePermissionDeniedError(
                message_class=message_class,
                permission_class=permission
            )
