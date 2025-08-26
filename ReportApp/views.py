from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ReportApp.models import Room
from ReportApp.algorithm.report_graph import ReportGraph
from ReportApp.algorithm.room_analyzer import RoomAnalyzer

from utils.custon_views.views import RawTemplateView

from RoomAccounting.settings import HOST, PORT, ROOM_ACCOUNTING_APP_BASE_URL


def landing_page(request):
    if not request.user.is_anonymous:
        return home(request)

    context = {'HOST': HOST, 'PORT': PORT, 'app_base_url': ROOM_ACCOUNTING_APP_BASE_URL}
    return render(request, 'index.html', context=context)


class HomeView(RawTemplateView):
    template_name = "list_items/room_options.html"
    
    def get(self, request):
        user = request.user
        rooms = Room.objects.filter(creator=user).order_by("created_at")
        context = {'HOST': HOST, 'PORT': PORT, 'app_base_url': ROOM_ACCOUNTING_APP_BASE_URL,
                   'username': user.username, 'rooms': rooms}
        return self.render_to_response(context)


class FinalReportView(RawTemplateView):
    template_name = "list_items/final_result.html"
    
    def get(self, request, room_id):
        if request.user.is_anonymous:
            return self._render_result("Please sign in")

        room = Room.objects.get(id=room_id)
        if room not in request.user.room_set.all():
            return self._render_result("You're not the owner of the room")

        report_graph = ReportGraph(room)
        cleared = RoomAnalyzer.is_room_cleared(report_graph)

        context = {'result_graph': report_graph,
                   'mode': 'report_for_clearing',
                   'room_name': room.name,
                   'cleared': cleared}
        return self.render_to_response(context)
    
    
    def _render_result(request, result):
        return render(request, 'result.html', context={'result': result})


class FinalReportAPI(APIView):
    
    def post(self, request):
        room_id = request.data['room_id']
        room = Room.objects.get(id=room_id)

        report_graph = ReportGraph(room)
        return Response(report_graph.edges_sorted, status=status.HTTP_200_OK)
