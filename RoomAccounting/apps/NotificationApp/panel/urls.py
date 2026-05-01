from django.urls import path
from .views import channels


urlpatterns = [
    path("channels/", channels.channel_list_view, name="manage_channels"),
    
    path("channels/create/", channels.create_channel_view, name="panel_channel_create"),
    path("channels/<int:channel_id>/delete/", channels.delete_channel_view, name="panel_channel_delete"),
    path("channels/<int:channel_id>/make-primary/", channels.make_primary_view, name="panel_channel_primary"),
    path("channels/<int:channel_id>/set-priority/", channels.set_priority_view, name="panel_channel_priority"),
]
