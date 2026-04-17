from django.utils import timezone

from ......models import NotificationToken


def get_latest_valid_otp_token(selector: str):
    return (
        NotificationToken.objects
        .filter(
            selector=selector,
            purpose="otp",
            is_used=False,
            expires_at__gt=timezone.now(),
        )
        .order_by("-created_at")
        .first()
    )
