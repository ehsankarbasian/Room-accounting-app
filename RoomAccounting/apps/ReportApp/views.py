from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.base import View

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.ReportApp.models import Room, Transaction, Spend
from apps.ReportApp.graph_core import ReportFacade

from utils.custom_views.views import RawTemplateView
from utils.custom_views.mixins import PaginationMixin

from apps.AuthApp.persmissions.mixins import PermissionMixin
from apps.AuthApp.persmissions.permissions import IsAuthenticated, AllowAny

from apps.NotificationContribApp.services import AuthNotifications, SecurityNotifications
from apps.NotificationContribApp.notification_types import SenderType


class LandingPageView(PermissionMixin, RawTemplateView):
    permission_classes = (AllowAny, )
    template_name = "index.html"
    
    def get(self, request):
        if not request.user.is_anonymous:
            return redirect(reverse('ReportApp:home'))

        return self.render_to_response(context=None)


class HomeView(PermissionMixin, RawTemplateView):
    permission_classes = (IsAuthenticated, )
    template_name = "ReportApp/lists/rooms.html"
    
    def get(self, request):
        user = request.user
        
        rooms = (
            Room.objects.filter(creator=user)
            .prefetch_related("person_set")
            .order_by("created_at")
        )

        context = {'username': user.username, 'rooms': rooms}
        return self.render_to_response(context)


# TODO: use ListView
class SpendListView(PermissionMixin, PaginationMixin, RawTemplateView):
    permission_classes = (IsAuthenticated, )
    template_name = 'ReportApp/lists/spends.html'
    page_size = 6
    
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id, creator__id=request.user.id)
        
        spends = (
            Spend.objects.prefetch_with_spenders_and_partners()
            .filter(room=room)
            .order_by('-date')
        )
        
        page_object = self.get_paginated_items(request, spends)
        context = {'spends': page_object, 'room_name': room.name}
        return self.render_to_response(context)


# TODO: use ListView
class TransactionListView(PermissionMixin, PaginationMixin, RawTemplateView):
    template_name = 'ReportApp/lists/transactions.html'
    permission_classes = (IsAuthenticated, )
    page_size = 8
    
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id, creator__id=request.user.id)
        
        transactions = (
            Transaction.objects.filter_by_room(room)
            .select_related_payer_and_receiver()
            .order_by('-date')
        )
        
        page_object = self.get_paginated_items(request, transactions)
        context = {'transactions': page_object, 'room_name': room.name}
        return self.render_to_response(context)


# TODO: use ListView if possible
class RoomLogView(PermissionMixin, PaginationMixin, RawTemplateView):
    template_name = 'ReportApp/lists/room_log.html'
    permission_classes = (IsAuthenticated, )
    page_size = 8
    
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id, creator__id=request.user.id)
        
        log = self._get_all_log(room)
        log = self.get_paginated_items(request, log)

        context = {'log': log, 'room_name': room.name}
        return self.render_to_response(context)
    
    
    def _get_all_log(self, room: Room):
        
        transactions = (
            Transaction.objects.filter_by_room(room)
            .select_related_payer_and_receiver()
            .order_by('-date')
        )
        
        spends = (
            Spend.objects.prefetch_with_spenders_and_partners()
            .filter(room=room)
            .order_by('-date')
        )

        log = sorted(chain(transactions, spends),
                    key=lambda item: item.date,
                    reverse=True)
        return log


class FinalReportView(PermissionMixin, RawTemplateView):
    permission_classes = (IsAuthenticated, )
    template_name = "ReportApp/lists/report.html"
    
    def get(self, request, room_id):
        room = (
            get_object_or_404(Room.objects.prefetch_related("person_set"),
                              id=room_id, 
                              creator__id=request.user.id)
        )
        persons = {person.id: person for person in room.person_set.all()}
        
        report_graph = ReportFacade.get_graph(room)
        cleared = ReportFacade.is_room_cleared(report_graph)

        context = {'result_graph': report_graph,
                   'room_name': room.name,
                   'persons': persons,
                   'cleared': cleared}
        return self.render_to_response(context)
    
    
    def _render_result(request, result):
        return render(request, 'result.html', context={'result': result})


class FinalReportAPI(PermissionMixin, APIView):
    # permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        # BUG: User can see another user report
        room_id = request.data['room_id']
        room = get_object_or_404(Room, id=room_id, creator__id=request.user.id)

        report_graph = ReportFacade.get_graph(room)
        return Response(report_graph._graph_schema, status=status.HTTP_200_OK)


class ReportEmailView(PermissionMixin, View):
    
    def post(self, request):
        
        AuthNotifications.send_otp(user=request.user, code=123, channel_name=SenderType.BALE)
        # SecurityNotifications.send_reset_password(user=request.user, token="__TOKEN__")
        
        result = request.POST
        return render(request, 'result.html', context={'result': result})
