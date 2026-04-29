from ...models import NotificationChannel

from .exceptions import ChannelNotFound


# TODO: reorder_channels


def set_priority(channel_id, priority):
    
    try:
        channel = NotificationChannel.objects.get(id=channel_id)
    except NotificationChannel.DoesNotExist:
        raise ChannelNotFound()

    channel.priority = priority
    channel.save(update_fields=["priority", "updated_at"])

    return channel


def normalize_priorities(recipient):
    
    channels = NotificationChannel.objects.filter(
        recipient_content_type=recipient._meta.app_label,
        recipient_object_id=recipient.pk,
    ).order_by("priority")

    for index, channel in enumerate(channels):
        channel.priority = index * 10
        channel.save(update_fields=["priority"])
