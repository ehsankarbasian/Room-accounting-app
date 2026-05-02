from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse

from ...registry.sender import SenderRegistry
from ...panel.services import channels


def channel_list_view(request):
    recipient = request.user

    channel_list = channels.list_recipient_channels(recipient)

    return render(
        request,
        "panel/channels/list.html",
        {
            "channels": channel_list
        }
    )


def create_channel_view(request):
    recipient = request.user

    if request.method == "POST":

        channel_type = request.POST.get("channel_type")
        identifier = request.POST.get("identifier")
        priority = request.POST.get("priority")

        channels.create_channel(
            recipient=recipient,
            channel_type=channel_type,
            identifier=identifier,
            priority=int(priority)
        )

        response = HttpResponse()
        response['HX-Refresh'] = 'true'
        return response

    registered_channel_types = SenderRegistry.get_registered_types()
    context = {"channel_types": registered_channel_types}
    
    return render(request, "panel/channels/create_form.html", context)


def delete_channel_view(request, channel_id):

    recipient = request.user

    try:
        channels.delete_channel(channel_id, recipient)
    except channels.ChannelNotFound:
        pass

    response = HttpResponse()
    response['HX-Refresh'] = 'true'
    return response


def update_channel_priority_view(request, channel_id):
    
    # TODO (Pre Drag&Drop option): Implement priority normalization to avoid collisions and maintain sequential order.

    if request.method == "POST":

        priority = request.POST.get("priority")

        channels.set_priority(
            channel_id=channel_id,
            priority=int(priority),
        )

    response = HttpResponse()
    response['HX-Refresh'] = 'true'
    return response


def make_primary_view(request, channel_id):

    recipient = request.user
    channel = channels.get_channel(channel_id, recipient)
    
    if not channel.is_verified:
        return HttpResponseBadRequest("Channel must be verified")
    
    channels.mark_as_primary(channel_id, recipient)
    
    response = HttpResponse()
    response['HX-Refresh'] = 'true'
    return response
