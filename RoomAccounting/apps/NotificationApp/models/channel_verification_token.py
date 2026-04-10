from django.db import models


class ChannelVerificationToken(models.Model):
    """
    Association between a notification channel and a token.
    """

    token = models.ForeignKey(
        "NotificationApp.NotificationToken",
        on_delete=models.CASCADE,
        related_name="channel_links",
    )

    channel = models.ForeignKey(
        "NotificationApp.NotificationChannel",
        on_delete=models.CASCADE,
        related_name="token_links",
    )

    class Meta:
        unique_together = ("token", "channel")
