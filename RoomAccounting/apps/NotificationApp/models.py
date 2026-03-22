from django.db import models

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings

from apps.NotificationApp.registry import SenderRegistry


class NotificationChannel(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_channels",
        verbose_name=_("User"),
    )
    
    channel_type = models.CharField(
        null=True,
        max_length=50,
        verbose_name=_("Channel Type"),
    )

    identifier = models.CharField(
        max_length=255,
        verbose_name=_("Destination"),
        help_text=_("Email address, phone number, chat id or etc ..."),
    )

    priority = models.PositiveIntegerField(
        default=100,
        help_text="Lower value means higher priority",
    )
    
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("Is Verified"),
        help_text=_("True when user has confirmed this channel"),
    )
    
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Is Primary"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "channel_type", "identifier")
        verbose_name = _("Notification Channel")
        verbose_name_plural = _("Notification Channels")

    def __str__(self):
        return f"{self.get_method_type_display()} ({self.identifier})"

    @property
    def display_name(self) -> str:
        return f"{self.get_method_type_display()} - {self.identifier}"
    
    def clean(self):
        super().clean()
        if not SenderRegistry.exists(self.channel_type):
            raise ValidationError(
                {"channel_type": _("Unsupported channel type: %(type)s") % {"type": self.channel_type}}
            )
