from django.shortcuts import render
from .helper_functions import result_page

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from AccountingApp.models import *
from .core_algorithm import calculate_result, simple_result


def report_for_clearing(request, room_id):
    if request.user.is_anonymous:
        return result_page(request, "Please sign in")

    room = Room.objects.get(id=room_id)
    if room not in request.user.room_set.all():
        return result_page(request, "You're not the owner of the room")

    # The core algorithm:
    final_dict = calculate_result(room)

    context = {'result': final_dict, 'mode': 'report_for_clearing', 'room_name': room.name}
    return render(request, 'log.html', context=context)


@api_view(['POST'])
def report_for_clearing_API(request):
    room_id = request.data['room_id']
    room = Room.objects.get(id=room_id)

    final_dict = calculate_result(room)
    final_dict = simple_result(final_dict)

    return Response(final_dict, status=status.HTTP_200_OK)
