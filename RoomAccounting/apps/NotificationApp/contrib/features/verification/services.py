import secrets
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django.apps import apps
from django.conf import settings
from django.contrib.auth.hashers import make_password

from ....models import NotificationToken, ChannelVerificationToken
from ....token_generator import TokenGenerator
from .messages.messages import VerifyChannelMessage
from ....dispatching.dispatcher import NotificationDispatcher


class VerificationService:

    DEFAULT_EXPIRATION_MINUTES = 30

    @classmethod
    def send_verification(cls, channel):

        # selector + secret (raw token)
        selector = secrets.token_hex(8)
        secret = TokenGenerator.generate()

        # hash only the secret
        hashed_token = make_password(secret)

        token = NotificationToken.objects.create(
            # channel=channel,
            selector=selector,
            token_hash=hashed_token,
            expires_at=timezone.now() + timedelta(minutes=cls.DEFAULT_EXPIRATION_MINUTES),
        )
        
        ChannelVerificationToken.objects.create(
            token=token,
            channel=channel,
        )

        # raw token sent to user (selector.secret)
        raw_token = f"{selector}.{secret}"

        verification_url = cls._build_verification_url(raw_token)

        data = VerifyChannelMessage.Data(
            verification_url=verification_url,
            verification_token=raw_token,
        )

        NotificationDispatcher.send(
            recipient=cls._get_recipient(channel),
            message_class=VerifyChannelMessage,
            data=data,
            explicit_channel=channel,
            is_verified=False,
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
