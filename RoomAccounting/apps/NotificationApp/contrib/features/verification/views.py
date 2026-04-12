from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.db import transaction

from ....models import ChannelVerificationToken


def verification_view(request, token):
    
    try:
        selector, secret = token.split(".")
    except ValueError:
        return HttpResponse("Invalid token format", status=400)

    channel_token = get_object_or_404(
        ChannelVerificationToken.objects.select_related("token", "channel"),
        token__selector=selector,
        token__is_used=False,
    )

    notification_token = channel_token.token
    channel = channel_token.channel

    if notification_token is None or channel is None:
        return HttpResponse("Invalid or expired token", status=400)

    if notification_token.expires_at and notification_token.expires_at < timezone.now():
        return HttpResponse("Verification link expired", status=400)

    if not check_password(secret, notification_token.token_hash):
        return HttpResponse("Invalid or expired token", status=400)

    with transaction.atomic():
        if not channel.is_verified:
            channel.is_verified = True
            channel.save(update_fields=["is_verified"])

        notification_token.is_used = True
        notification_token.save(update_fields=["is_used"])

    return HttpResponse("Channel verified successfully")
