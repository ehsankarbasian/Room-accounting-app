from django.views.generic.base import View
from django.shortcuts import redirect, get_object_or_404

from apps.ReportApp.models import Room

from apps.AuthApp.persmissions.mixins import PermissionMixin
from apps.AuthApp.persmissions.permissions import IsAuthenticated


class AddRoomView(PermissionMixin, View):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        room_name = request.POST['room_name']
        Room.objects.create(name=room_name, creator=request.user)
        return redirect('ReportApp:home')


class DeleteRoomView(PermissionMixin, View):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id, creator__id=request.user.id)
        
        # TODO: 2 factor auth to delete the room
        room.delete()
        return redirect('ReportApp:home')


class EditRoomView(PermissionMixin, View):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id, creator__id=request.user.id)
        
        room.name = request.POST['room_name']
        room.save()
        return redirect('ReportApp:home')
