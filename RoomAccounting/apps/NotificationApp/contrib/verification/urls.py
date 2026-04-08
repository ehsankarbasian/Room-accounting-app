from django.urls import path

from .views import verify_channel

app_name = "NotificationApp"


urlpatterns = [
    path(
        "notifications/verify/<str:token>/",
        verify_channel,
        name="verify-channel",
    ),
]
