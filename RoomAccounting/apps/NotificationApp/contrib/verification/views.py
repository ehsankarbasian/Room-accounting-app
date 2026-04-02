from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404

from ...models import NotificationChannelVerification


def verify_channel(request, token):

    verification = get_object_or_404(
        NotificationChannelVerification,
        token=token,
        is_used=False,
    )

    if verification.expires_at < timezone.now():
        return HttpResponse("Verification link expired", status=400)

    channel = verification.channel

    channel.is_verified = True
    channel.save(update_fields=["is_verified"])

    verification.is_used = True
    verification.save(update_fields=["is_used"])

    return HttpResponse("Channel verified successfully")
