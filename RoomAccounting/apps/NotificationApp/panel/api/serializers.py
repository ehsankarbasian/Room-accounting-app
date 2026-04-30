from rest_framework import serializers

from ...models import NotificationChannel
from ...panel.services import channels


class ChannelReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationChannel
        fields = [
            "id",
            "channel_type",
            "identifier",
            "priority",
            "is_primary",
            "is_verified",
            "created_at",
        ]


class ChannelCreateSerializer(serializers.Serializer):

    channel_type = serializers.CharField()
    identifier = serializers.CharField()
    priority = serializers.IntegerField(required=False, default=100)

    def create(self, validated_data):

        request = self.context["request"]

        return channels.create_channel(
            recipient=request.user,
            channel_type=validated_data["channel_type"],
            identifier=validated_data["identifier"],
            priority=validated_data["priority"],
        )


class ChannelUpdateSerializer(serializers.Serializer):

    identifier = serializers.CharField()

    def update(self, instance, validated_data):

        return channels.update_identifier(
            channel_id=instance.id,
            new_identifier=validated_data["identifier"],
        )
