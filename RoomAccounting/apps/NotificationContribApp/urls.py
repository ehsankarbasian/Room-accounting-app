from django.urls import path

from .views import verify_channel


urlpatterns = [
    path(
        "notifications/verify/<str:token>/",
        verify_channel,
        name="verify-channel",
    ),
]
