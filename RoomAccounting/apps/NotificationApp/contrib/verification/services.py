from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django.apps import apps
from django.conf import settings

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
            recipient=cls._get_recipient(channel),
            message_class=VerifyChannelMessage,
            data=data,
            explicit_channel=channel,
        )
    
    
    @staticmethod
    def _get_recipient(channel):
        recipient_model = apps.get_model(
            channel.recipient_content_type.app_label,
            channel.recipient_content_type.model,
        )
        
        return recipient_model._base_manager.get(pk=channel.recipient_object_id)
    

    @staticmethod
    def _build_verification_url(token: str) -> str:
        
        path = reverse(
            "NotificationApp:verify-channel",
            kwargs={"token": token},
        )
        
        return f"{settings.SITE_BASE_URL}{path}"
