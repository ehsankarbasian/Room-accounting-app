from django.db import models

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from ..registry import SenderRegistry
from .managers import NotificationChannelQuerySet


class NotificationChannel(models.Model):
    """
    A delivery channel for a notification.

    Examples:
        - email address
        - phone number (SMS)
        - chat id (Telegram / WhatsApp)

    A recipient can have multiple channels per type, each with its own
    verification state and delivery priority.
    """
    
    objects = NotificationChannelQuerySet.as_manager()

    recipient_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Recipient Content Type"),
        null=False,
    )

    recipient_object_id = models.PositiveBigIntegerField(
        null=False,
    )

    recipient = GenericForeignKey(
        "recipient_content_type",
        "recipient_object_id",
    )

    # Channel type registered in SenderRegistry (e.g. EMAIL, SMS, TELEGRAM)
    channel_type = models.CharField(
        null=True,
        max_length=50,
        verbose_name=_("Channel Type"),
    )

    # Destination identifier for the channel
    # e.g. email address, phone number, chat id
    identifier = models.CharField(
        max_length=255,
        verbose_name=_("Destination"),
        help_text=_("Email address, phone number, chat id or etc ..."),
    )

    # Determines delivery order (lower = higher priority)
    priority = models.PositiveIntegerField(
        default=100,
        help_text="Lower value means higher priority",
    )

    # Indicates whether the recipient has confirmed ownership of this channel
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("Is Verified"),
        help_text=_("True when recipient has confirmed this channel"),
    )

    # Marks the recipient's preferred primary notification channel
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Is Primary"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "recipient_content_type",
            "recipient_object_id",
            "channel_type",
            "identifier",
        )

        verbose_name = _("Notification Channel")
        verbose_name_plural = _("Notification Channels")

        # Common query patterns used by ChannelResolver
        indexes = [
            models.Index(fields=["recipient_content_type", "recipient_object_id", "channel_type"]),
            models.Index(fields=["recipient_content_type", "recipient_object_id", "is_primary"]),
            models.Index(fields=["recipient_content_type", "recipient_object_id", "priority"]),
        ]

        # Ensures each recipient has at most one primary channel
        constraints = [
            models.UniqueConstraint(
                fields=["recipient_content_type", "recipient_object_id"],
                condition=models.Q(is_primary=True),
                name="unique_primary_channel_per_recipient",
            ),
        ]

    def __str__(self):
        return f"{self.recipient} - {self.channel_type} ({self.identifier})"

    def clean(self):
        """
        Validates that the channel_type is registered in SenderRegistry.
        Prevents storing unsupported channel types in the database.
        
        channel_type values are dynamically validated through SenderRegistry
        instead of Django choices to allow runtime pluggable channels.
        """
        
        super().clean()

        if not SenderRegistry.exists(self.channel_type):
            raise ValidationError(
                {"channel_type": _("Unsupported channel type: %(type)s") % {"type": self.channel_type}}
            )
