import hashlib
from datetime import timedelta
from django.utils import timezone

from .....dispatching.dispatcher import NotificationDispatcher
from .....models import NotificationToken

from .message import ForgotPasswordMessage


def send_forgot_password(user, code: str):
    
    data = ForgotPasswordMessage.Data(code=code, reset_password_url='test__')
    
    selector = f"user:{user.id}:reset_password"
    token_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()

    NotificationToken.objects.create(
        selector=selector,
        token_hash=token_hash,
        purpose="otp",
        expires_at=timezone.now() + timedelta(minutes=2),
    )

    NotificationDispatcher.send(
        user,
        ForgotPasswordMessage,
        data,
    )
