from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationToken(models.Model):
    """
    Core token entity used by the notification framework.

    This model represents a generic token instance independent
    from any specific use-case such as verification, password reset,
    OTP authentication, etc.

    Domain associations must be implemented via separate relation models.
    """

    selector = models.CharField(
        max_length=64,
        db_index=True,
    )

    token_hash = models.CharField(
        max_length=128,
    )

    purpose = models.CharField(
        max_length=64,
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
        verbose_name = _("Notification Token")
        verbose_name_plural = _("Notification Tokens")

        indexes = [
            models.Index(fields=["selector"]),
            models.Index(fields=["purpose", "is_used", "expires_at"]),
        ]
