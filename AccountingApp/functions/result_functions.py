from django.shortcuts import render, redirect
from .helper_functions import result_page, create_clearing_message, send_text_email

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from AccountingApp.models import *
from .core_algorithm import calculate_result, simple_result, is_room_cleared, related_result


def report_for_clearing(request, room_id):
    if request.user.is_anonymous:
        return result_page(request, "Please sign in")

    room = Room.objects.get(id=room_id)
    if room not in request.user.room_set.all():
        return result_page(request, "You're not the owner of the room")

    # The core algorithm:
    final_dict = calculate_result(room)
    cleared = is_room_cleared(final_dict)

    context = {'result': final_dict, 'mode': 'report_for_clearing', 'room_name': room.name, 'cleared': cleared}
    return render(request, 'log.html', context=context)


@api_view(['POST'])
def report_for_clearing_API(request):
    room_id = request.data['room_id']
    room = Room.objects.get(id=room_id)

    final_dict = calculate_result(room)
    final_dict = simple_result(final_dict)

    return Response(final_dict, status=status.HTTP_200_OK)


def send_result_email(request):
    room_id = request.POST['room_id']
    room = Room.objects.get(id=room_id)

    if request.user.is_anonymous:
        return result_page(request, "Please sign in")

    if room in request.user.room_set.all():

        final_dict = calculate_result(room)
        if is_room_cleared(final_dict):
            return result_page(request, "room is cleared")

        for person in room.person_set.all():
            ID = str(person.id)
            if "person" + ID in request.POST:
                content = related_result(final_dict, person.id)
                if content:
                    initial_message = "Hello dear " + person.name + "\n"\
                                      + "Room admin: " + person.room.creator.fullname + "\n"\
                                      + "Room admin email: " + person.room.creator.email + "\n"\
                                      + "Do the below payment please:"
                    message = create_clearing_message(content, initial_message)
                    if person.verified_email:
                        send_text_email("Bill of the room '" + room.name + "'", message, [person.email])

        return redirect('home')

    return result_page(request, "You're not the owner of the room")
