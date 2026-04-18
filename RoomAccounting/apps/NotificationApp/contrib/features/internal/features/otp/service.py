import hashlib
from datetime import timedelta
from django.utils import timezone

from ......dispatching.dispatcher import NotificationDispatcher
from ......models import NotificationToken

from .message import OtpMessage
from .query import get_latest_valid_otp_token


def send_otp(user, code: str, verify_otp_url: str):
    
    data = OtpMessage.Data(code=code, verify_otp_url=verify_otp_url)
    
    selector = f"user:{user.id}:otp"
    token_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()

    NotificationToken.objects.create(
        selector=selector,
        token_hash=token_hash,
        purpose="otp",
        expires_at=timezone.now() + timedelta(minutes=2),
    )

    NotificationDispatcher.send(
        recipient=user,
        message_class=OtpMessage,
        data=data,
    )


def verify_otp(user, code: str) -> bool:

    selector = f"user:{user.id}:otp"

    token = get_latest_valid_otp_token(selector)

    if not token:
        return False

    code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()

    if token.token_hash != code_hash:
        return False

    token.is_used = True
    token.save(update_fields=["is_used"])

    return True
