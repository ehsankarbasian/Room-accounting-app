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
        max_length=6,
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
        
        constraints = [
            models.UniqueConstraint(
                fields=["channel", "token"],
                name="unique_channel_token"
            )
        ]
        
        indexes = [
            models.Index(fields=["token"]),
        ]
