from django.urls import path

from . import views


urlpatterns = [
    path(
        "channels/",
        views.channels_collection_view,
        name="panel_channels",
    ),
    path(
        "channels/<int:channel_id>/",
        views.channel_detail_view,
        name="panel_channel_detail",
    ),
    path(
        "channels/<int:channel_id>/make-primary/",
        views.make_primary_channel_view,
        name="panel_channel_make_primary",
    ),
    path(
        "channels/<int:channel_id>/set-priority/",
        views.set_priority_channel_view,
        name="panel_channel_set_priority",
    ),
]
