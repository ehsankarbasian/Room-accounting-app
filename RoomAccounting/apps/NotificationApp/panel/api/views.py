from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from ...panel.services import channels

from .serializers import (
    ChannelReadSerializer,
    ChannelCreateSerializer,
    ChannelUpdateSerializer,
)


# TODO: Security hardening
# - Ensure channel ownership checks in all endpoints
# - Prevent users from accessing channels of other recipients

# TODO: DRF permissions
# - Add IsAuthenticated permission
# - Add custom permission for channel ownership if needed

# TODO: Exception mapping
# - Map service layer exceptions to proper HTTP responses
# - ChannelNotFound -> 404
# - DuplicateChannel -> 409
# - InvalidChannelType -> 400

# TODO: Validation improvements
# - Validate priority values
# - Prevent invalid state transitions

# TODO: API documentation
# - Add OpenAPI schema
# - Provide usage examples for frontend clients


@api_view(["GET", "POST"])
def channels_collection_view(request):

    if request.method == "GET":
        channel_list = channels.list_recipient_channels(request.user)
        serializer = ChannelReadSerializer(channel_list, many=True)
        return Response(serializer.data)

    serializer = ChannelCreateSerializer(
        data=request.data,
        context={"request": request},
    )

    serializer.is_valid(raise_exception=True)
    channel = serializer.save()

    return Response(
        ChannelReadSerializer(channel).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET", "PATCH", "DELETE"])
def channel_detail_view(request, channel_id):

    try:
        channel = channels.get_channel(channel_id)
    except channels.ChannelNotFound:
        raise NotFound("Channel not found")

    if request.method == "GET":
        serializer = ChannelReadSerializer(channel)
        return Response(serializer.data)

    if request.method == "PATCH":
        serializer = ChannelUpdateSerializer(
            instance=channel,
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)
        updated_channel = serializer.save()
        return Response(ChannelReadSerializer(updated_channel).data)

    channels.delete_channel(channel_id)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def make_primary_channel_view(request, channel_id):

    channels.mark_as_primary(channel_id)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def set_priority_channel_view(request, channel_id):

    priority = request.data.get("priority")
    channels.set_priority(channel_id, priority)
    return Response(status=status.HTTP_204_NO_CONTENT)
