from django import forms
from django.contrib import admin

from .models import (
    NotificationChannel,
    NotificationToken,
    ChannelVerificationToken,
)
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


class ChannelVerificationTokenInline(admin.TabularInline):

    model = ChannelVerificationToken
    extra = 0
    autocomplete_fields = ("token",)


@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):

    form = NotificationChannelAdminForm

    inlines = [
        ChannelVerificationTokenInline,
    ]

    list_display = (
        "id",
        "recipient",
        "channel_type",
        "identifier",
        "priority",
        "is_primary",
        "is_verified",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "channel_type",
        "is_primary",
        "is_verified",
    )

    search_fields = (
        "identifier",
    )


class ChannelVerificationTokenInlineForToken(admin.TabularInline):

    model = ChannelVerificationToken
    extra = 0
    autocomplete_fields = ("channel",)


@admin.register(NotificationToken)
class NotificationTokenAdmin(admin.ModelAdmin):

    inlines = [
        ChannelVerificationTokenInlineForToken,
    ]

    list_display = (
        "id",
        "selector",
        "token_hash",
        "purpose",
        "is_used",
        "created_at",
        "expires_at",
    )

    list_filter = (
        "purpose",
        "is_used",
    )

    search_fields = (
        "selector",
    )


@admin.register(ChannelVerificationToken)
class ChannelVerificationTokenAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "channel",
        "token",
    )

    search_fields = (
        "token__selector",
        "channel__identifier",
    )
