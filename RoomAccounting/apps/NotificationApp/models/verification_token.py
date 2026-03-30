import secrets
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class NotificationChannelVerification(models.Model):

    channel = models.ForeignKey(
        "NotificationApp.NotificationChannel",
        on_delete=models.CASCADE,
        related_name="verifications",
    )

    token = models.CharField(
        max_length=128,
        unique=True,
        db_index=True,
    )

    is_used = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = _("Notification Channel Verification")
        verbose_name_plural = _("Channel Verification Tokens")
        
        indexes = [
            models.Index(fields=["token"]),
        ]

    @classmethod
    def create_for_channel(cls, channel):

        token = secrets.token_urlsafe(32)

        verification = cls.objects.create(
            channel=channel,
            token=token,
            expires_at=timezone.now() + timedelta(hours=24),
        )

        return verification
