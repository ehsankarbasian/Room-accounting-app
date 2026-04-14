import hashlib
from datetime import timedelta
from django.utils import timezone

from .....dispatching.dispatcher import NotificationDispatcher
from .....models import NotificationToken

from .message import OtpMessage


@staticmethod
def send_otp(user, code: str):
    
    data = OtpMessage.Data(code=code)
    
    token_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()

    NotificationToken.objects.create(
        selector=str(user.id),
        token_hash=token_hash,
        purpose="otp",
        expires_at=timezone.now() + timedelta(minutes=2),
    )

    NotificationDispatcher.send(
        user,
        OtpMessage,
        data,
    )
