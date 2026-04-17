from django.utils import timezone

from ......models import NotificationToken


def get_latest_valid_reset_password_token(selector: str):
    return (
        NotificationToken.objects
        .filter(
            selector=selector,
            purpose="reset_password",
            is_used=False,
            expires_at__gt=timezone.now(),
        )
        .order_by("-created_at")
        .first()
    )
