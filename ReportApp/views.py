from itertools import chain

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q
from ReportApp.models import Room, Transaction
from ReportApp.algorithm import ReportFacade

from utils.custom_views.views import RawTemplateView
from utils.custom_views.mixins import PaginationMixin

from AuthApp.persmissions.mixins import PermissionMixin
from AuthApp.persmissions.permissions import IsAuthenticated, AllowAny


class LandingPageView(PermissionMixin, RawTemplateView):
    permission_classes = (AllowAny, )
    template_name = "index.html"
    
    def get(self, request):
        if not request.user.is_anonymous:
            return redirect(reverse('ReportApp:home'))

        return self.render_to_response(context=None)


class HomeView(PermissionMixin, RawTemplateView):
    permission_classes = (IsAuthenticated, )
    template_name = "OperationApp/room_options.html"
    
    def get(self, request):
        user = request.user
        rooms = Room.objects.filter(creator=user).order_by("created_at")
        context = {'username': user.username, 'rooms': rooms}
        return self.render_to_response(context)


# TODO: use ListView
class SpendListView(PermissionMixin, PaginationMixin, RawTemplateView):
    permission_classes = (IsAuthenticated, )
    template_name = 'ReportApp/spends.html'
    page_size = 6
    
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        if not room.is_owner(request.user):
            return _result_page(request, "You're not the owner of the room")
        
        spends = room.spend_set.all().order_by('-date')
        
        page_object = self.get_paginated_items(request, spends)
        context = {'spends': page_object, 'room_name': room.name}
        return self.render_to_response(context)


# TODO: use ListView
class TransactionListView(PermissionMixin, PaginationMixin, RawTemplateView):
    template_name = 'ReportApp/transactions.html'
    permission_classes = (IsAuthenticated, )
    page_size = 8
    
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)

        if not room.is_owner(request.user):
            return _result_page(request, "You're not the owner of the room")
    
        persons = room.person_set.all()
        payer_query = Q(payer__in=persons)
        receiver_query = Q(receiver__in=persons)
        transactions = Transaction.objects.filter(payer_query | receiver_query).order_by('-date')

        page_object = self.get_paginated_items(request, transactions)
        context = {'transactions': page_object, 'room_name': room.name}
        return self.render_to_response(context)


# TODO: use ListView if possible
class RoomLogView(PermissionMixin, PaginationMixin, RawTemplateView):
    template_name = 'ReportApp/room_log.html'
    permission_classes = (IsAuthenticated, )
    page_size = 8
    
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)

        if not room.is_owner(request.user):
            return _result_page(request, "You're not the owner of the room")
        
        log = self._room_log_helper(room)
        log = self.get_paginated_items(request, log)

        context = {'log': log, 'room_name': room.name}
        return self.render_to_response(context)
    
    
    def _room_log_helper(self, room):
        transactions = room.transaction_set
        spends = room.spend_set.all().order_by('-date')

        log = sorted(chain(transactions, spends),
                    key=lambda item: item.date,
                    reverse=True)
        return log


class FinalReportView(PermissionMixin, RawTemplateView):
    permission_classes = (IsAuthenticated, )
    template_name = "ReportApp/final_result.html"
    
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        if not room.is_owner(request.user):
            return self._render_result("You're not the owner of the room")

        report_graph = ReportFacade.get_graph(room)
        cleared = ReportFacade.is_room_cleared(report_graph)

        context = {'result_graph': report_graph,
                   'mode': 'report_for_clearing',
                   'room_name': room.name,
                   'cleared': cleared}
        return self.render_to_response(context)
    
    
    def _render_result(request, result):
        return render(request, 'result.html', context={'result': result})


class FinalReportAPI(PermissionMixin, APIView):
    # permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        # BUG: User can se onother user report
        room_id = request.data['room_id']
        room = Room.objects.get(id=room_id)

        report_graph = ReportFacade.get_graph(room)
        return Response(report_graph._graph_schema, status=status.HTTP_200_OK)


class ReportEmailView(PermissionMixin, View):
    pass


def _result_page(request, result):
    return render(request, 'result.html', context={'result': result})
