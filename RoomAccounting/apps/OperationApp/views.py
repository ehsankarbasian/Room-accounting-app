from secrets import token_hex
from random import randint

from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import View
from django.db import transaction
from django.contrib.auth import get_user_model

from apps.ReportApp.models import Room, Person

from apps.AuthApp.persmissions.mixins import PermissionMixin
from apps.AuthApp.persmissions.permissions import IsAuthenticated

from apps.NotificationContribApp.senders import SmsSender, EmailSender
from apps.NotificationApp.models import NotificationChannel


User = get_user_model()


# TODO: Use ModelViews to CRUD


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


class AddPersonView(PermissionMixin, View):
    permission_classes = (IsAuthenticated, )
    
    @transaction.atomic
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id, creator__id=request.user.id)
        
        name = request.POST['person_name']
        email = request.POST['email']
        phone = request.POST['phone']

        user = User.objects.create(
            username=email,
            email=email,
            phone_number=phone,
            fullname=name,
            role=User.Role.PERSON
        )
        
        Person.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone,
            room=room,
            verify_email_token=token_hex(64),
            verify_phone_code=randint(100000, 999999)
        )

        NotificationChannel.objects.create(
            identifier=phone,
            channel_type=SmsSender.sender_key,
            recipient=user
        )
        NotificationChannel.objects.create(
            identifier=email,
            channel_type=EmailSender.sender_key,
            recipient=user
        )

        return redirect('ReportApp:home')
