from ...models import NotificationChannel

from .exceptions import ChannelNotFound


# TODO: disable/enable channel


def delete_channel(channel_id, recipient):
    
    try:
        channel = NotificationChannel.objects.get(id=channel_id)
    except NotificationChannel.DoesNotExist:
        raise ChannelNotFound()

    channel.delete()


def update_identifier(channel_id, new_identifier):
    
    try:
        channel = NotificationChannel.objects.get(id=channel_id)
    except NotificationChannel.DoesNotExist:
        raise ChannelNotFound()

    channel.identifier = new_identifier
    channel.is_verified = False
    channel.save(update_fields=["identifier", "is_verified", "updated_at"])

    return channel


def mark_as_primary(channel_id, recipient):
    
    try:
        channel = NotificationChannel.objects.get(id=channel_id)
    except NotificationChannel.DoesNotExist:
        raise ChannelNotFound()

    NotificationChannel.objects.filter(
        recipient_content_type=channel.recipient_content_type,
        recipient_object_id=channel.recipient_object_id,
        is_primary=True,
    ).update(is_primary=False)

    channel.is_primary = True
    channel.save(update_fields=["is_primary", "updated_at"])

    return channel
