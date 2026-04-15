import hashlib
from datetime import timedelta

from django.utils import timezone
from django.urls import reverse
from django.conf import settings

from .....dispatching.dispatcher import NotificationDispatcher
from .....models import NotificationToken

from .message import ForgotPasswordMessage
from .views import forgot_password_view


def send_forgot_password(user, code: str):
    
    url = _build_verification_url(token=code)
    data = ForgotPasswordMessage.Data(code=code, reset_password_url=url)
    
    selector = f"user:{user.id}:reset_password"
    token_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()

    NotificationToken.objects.create(
        selector=selector,
        token_hash=token_hash,
        purpose="reset_password",
        expires_at=timezone.now() + timedelta(minutes=2),
    )

    NotificationDispatcher.send(
        user,
        ForgotPasswordMessage,
        data,
    )


def _build_verification_url(token: str) -> str:
    
    path = reverse(
        forgot_password_view.url_name,
        kwargs={"token": token},
    )
    
    return f"{settings.SITE_BASE_URL}{path}"
