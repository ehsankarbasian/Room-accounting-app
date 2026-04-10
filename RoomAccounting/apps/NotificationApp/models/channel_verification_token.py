from django.db import models


class ChannelVerificationToken(models.Model):
    """
    Association between a notification channel and a token.
    """

    token = models.ForeignKey(
        "NotificationApp.NotificationToken",
        on_delete=models.CASCADE,
        related_name="channel_links",
        null=True,
        blank=True,
    )

    channel = models.ForeignKey(
        "NotificationApp.NotificationChannel",
        on_delete=models.CASCADE,
        related_name="token_links",
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ("token", "channel")

        indexes = [
            models.Index(fields=["channel"]),
            models.Index(fields=["token"]),
        ]
