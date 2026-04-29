from django.contrib.contenttypes.models import ContentType

from ...models import NotificationChannel
from ...registry.sender import SenderRegistry

from .exceptions import ChannelAlreadyExists, UnsupportedChannelType


def create_channel(recipient, channel_type, identifier, priority=100):
    
    if not SenderRegistry.exists(channel_type):
        raise UnsupportedChannelType(channel_type)

    recipient_content_type = ContentType.objects.get_for_model(recipient)

    exists = NotificationChannel.objects.filter(
        recipient_content_type=recipient_content_type,
        recipient_object_id=recipient.pk,
        channel_type=channel_type,
        identifier=identifier,
    ).exists()

    if exists:
        raise ChannelAlreadyExists()

    channel = NotificationChannel.objects.create(
        recipient_content_type=recipient_content_type,
        recipient_object_id=recipient.pk,
        channel_type=channel_type,
        identifier=identifier,
        priority=priority,
    )

    return channel
