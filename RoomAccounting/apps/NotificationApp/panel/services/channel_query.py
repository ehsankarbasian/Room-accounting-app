from django.contrib.contenttypes.models import ContentType

from ...models import NotificationChannel

from .exceptions import ChannelNotFound


def list_recipient_channels(recipient):
    
    recipient_content_type = ContentType.objects.get_for_model(recipient)

    return NotificationChannel.objects.filter(
        recipient_content_type=recipient_content_type,
        recipient_object_id=recipient.pk,
    ).order_by("priority")


def get_channel(channel_id):
    
    try:
        return NotificationChannel.objects.get(id=channel_id)
    except NotificationChannel.DoesNotExist:
        raise ChannelNotFound()


def get_primary_channel(recipient):
    
    recipient_content_type = ContentType.objects.get_for_model(recipient)

    return NotificationChannel.objects.filter(
        recipient_content_type=recipient_content_type,
        recipient_object_id=recipient.pk,
        is_primary=True,
    ).first()
