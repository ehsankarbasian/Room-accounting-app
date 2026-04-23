from django.db.models.signals import post_save
from django.dispatch import receiver

from ......models import NotificationChannel
from ......registry.sender import SenderRegistry

from .dispatch_config import register_verify_message_options_for_channel
from .service import VerificationService


@receiver(post_save, sender=NotificationChannel)
def trigger_channel_verification(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.is_verified:
        return

    sender_class = SenderRegistry.get(instance.channel_type)
    register_verify_message_options_for_channel(channel=sender_class)
    VerificationService.send_verification(instance)
