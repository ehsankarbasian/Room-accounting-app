from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.hashers import check_password

from ...models import NotificationToken


def verify_channel(request, token):

    try:
        selector, secret = token.split(".")
    except ValueError:
        return HttpResponse("Invalid token format", status=400)

    verification = get_object_or_404(
        NotificationToken.objects.select_related("channel"),
        selector=selector,
        is_used=False,
    )

    if verification.expires_at < timezone.now():
        return HttpResponse("Verification link expired", status=400)

    # check hashed secret
    if not check_password(secret, verification.token):
        return HttpResponse("Invalid or expired token", status=400)

    channel = verification.channel

    if not channel.is_verified:
        channel.is_verified = True
        channel.save(update_fields=["is_verified"])

    verification.is_used = True
    verification.save(update_fields=["is_used"])

    return HttpResponse("Channel verified successfully")
