from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ReportApp.models import Room
from ReportApp.algorithm.report_graph import ReportGraph
from ReportApp.algorithm.room_analyzer import RoomAnalyzer

from RoomAccounting.settings import HOST, PORT, ROOM_ACCOUNTING_APP_BASE_URL


def _result_page(request, result):
    return render(request, 'result.html', context={'result': result})


def landing_page(request):
    if not request.user.is_anonymous:
        return home(request)

    context = {'HOST': HOST, 'PORT': PORT, 'app_base_url': ROOM_ACCOUNTING_APP_BASE_URL}
    return render(request, 'index.html', context=context)


def home(request):
    user = request.user
    rooms = Room.objects.filter(creator=user).order_by("created_at")
    context = {'HOST': HOST, 'PORT': PORT, 'app_base_url': ROOM_ACCOUNTING_APP_BASE_URL,
               'username': user.username, 'rooms': rooms}
    return render(request, 'home.html', context=context)


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
