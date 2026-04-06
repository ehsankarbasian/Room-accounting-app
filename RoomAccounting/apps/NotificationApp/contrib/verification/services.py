from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from ...models import NotificationChannelVerification
from .tokens import VerificationTokenGenerator
from .messages.messages import VerifyChannelMessage
from ...dispatching.dispatcher import NotificationDispatcher


class VerificationService:

    DEFAULT_EXPIRATION_MINUTES = 30

    @classmethod
    def send_verification(cls, channel):

        raw_token = VerificationTokenGenerator.generate()

        NotificationChannelVerification.objects.create(
            channel=channel,
            token=raw_token,
            expires_at=timezone.now() + timedelta(minutes=cls.DEFAULT_EXPIRATION_MINUTES),
        )

        verification_url = cls._build_verification_url(raw_token)

        data = VerifyChannelMessage.Data(
            verification_url=verification_url
        )

        NotificationDispatcher.send(
            recipient=channel.recipient,
            message_class=VerifyChannelMessage,
            data=data,
            channel_override=channel.channel_type,
        )

    @staticmethod
    def _build_verification_url(token: str) -> str:
        
        return '__TODO__'

        # return reverse(
        #     "apps.notificationapp:verify-channel",
        #     kwargs={"token": token},
        # )
