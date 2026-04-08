from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationChannelVerification(models.Model):

    channel = models.ForeignKey(
        "NotificationApp.NotificationChannel",
        on_delete=models.CASCADE,
        related_name="verifications",
    )

    # Selector for database lookup
    selector = models.CharField(
        max_length=32,
        db_index=True,
        null=False,
        blank=False,
    )

    # hashed secret stored here
    token = models.CharField(max_length=128)

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
            models.Index(fields=["channel", "is_used", "expires_at"]),
            models.Index(fields=["selector"]),  # ensure fast lookup
        ]
