import hashlib
from datetime import timedelta

from django.utils import timezone
from django.urls import reverse
from django.conf import settings

from ......dispatching.dispatcher import NotificationDispatcher
from ......models import NotificationToken

from .message import ForgotPasswordMessage


def send_forgot_password(user, code: str, current_namespace: str):
    
    url = _build_verification_url(current_namespace)
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
        recipient=user,
        message_class=ForgotPasswordMessage,
        data=data,
    )


def _build_verification_url(current_namespace) -> str:
    from .views import ResetPasswordByToken
    
    path = reverse(
        f"{current_namespace}:{ResetPasswordByToken.url_name}",
    )
    
    return f"{settings.SITE_BASE_URL}{path}"
