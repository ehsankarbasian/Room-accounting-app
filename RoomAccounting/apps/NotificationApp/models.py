from django.db import models

from django.utils.translation import gettext_lazy as _

from django.conf import settings


class NotificationMethod(models.Model):

    class MethodType(models.TextChoices):
        # TODO: update
        EMAIL = "email", _("Email")
        SMS = "sms", _("SMS")
        # TELEGRAM = "telegram", _("Telegram")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_methods",
        verbose_name=_("User"),
    )

    method_type = models.CharField(
        max_length=20,
        choices=MethodType.choices,
        verbose_name=_("Method Type"),
    )

    identifier = models.CharField(
        max_length=255,
        verbose_name=_("Destination"),
        help_text=_("Email address, phone number, chat id or etc ..."),
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
        unique_together = ("user", "method_type", "identifier")
        verbose_name = _("Notification Method")
        verbose_name_plural = _("Notification Methods")

    def __str__(self):
        return f"{self.get_method_type_display()} ({self.identifier})"

    @property
    def display_name(self) -> str:
        return f"{self.get_method_type_display()} - {self.identifier}"
