from django.db.models.signals import post_save
from django.dispatch import receiver

from .....models import NotificationChannel
from .services import VerificationService


@receiver(post_save, sender=NotificationChannel)
def trigger_channel_verification(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.is_verified:
        return

    VerificationService.send_verification(instance)
