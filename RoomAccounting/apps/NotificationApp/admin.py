from django import forms
from django.contrib import admin

from .models import NotificationChannel, NotificationToken
from .registry import SenderRegistry


class NotificationChannelAdminForm(forms.ModelForm):

    class Meta:
        model = NotificationChannel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices = [
            (key, key)
            for key in SenderRegistry.get_registered_types()
        ]

        self.fields["channel_type"].widget = forms.Select(choices=choices)


@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):

    form = NotificationChannelAdminForm

    list_display = (
        "id",
        "recipient",
        "channel_type",
        "identifier",
        "priority",
        "is_primary",
        "is_verified",
    )

    list_filter = (
        "channel_type",
        "is_primary",
        "is_verified",
    )

    search_fields = (
        "identifier",
    )


@admin.register(NotificationToken)
class NotificationChannelVerificationAdmin(admin.ModelAdmin):
    
    list_display = (
        "id",
        "token_hash",
        "is_used",
        "created_at",
        "expires_at",
    )

    list_filter = (
        "is_used",
    )

    search_fields = (
        "token",
    )
