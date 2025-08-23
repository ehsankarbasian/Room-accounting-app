from django.shortcuts import render, redirect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from AccountingApp.models import Room
from AccountingApp.views import _result_page

from AccountingApp.algorithm.report_graph import ReportGraph
from AccountingApp.algorithm.room_analyzer import RoomAnalyzer


def report_for_clearing(request, room_id):
    if request.user.is_anonymous:
        return _result_page(request, "Please sign in")

    room = Room.objects.get(id=room_id)
    if room not in request.user.room_set.all():
        return _result_page(request, "You're not the owner of the room")

    result_graph = ReportGraph(room)
    cleared = RoomAnalyzer.is_room_cleared(result_graph)

    context = {'result_graph': result_graph, 'mode': 'report_for_clearing', 'room_name': room.name, 'cleared': cleared}
    return render(request, 'list_items/final_result.html', context=context)


@api_view(['POST'])
def report_for_clearing_API(request):
    room_id = request.data['room_id']
    room = Room.objects.get(id=room_id)

    final_dict = ReportGraph(room)

    return Response(final_dict, status=status.HTTP_200_OK)
