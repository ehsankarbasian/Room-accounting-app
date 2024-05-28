from django.shortcuts import render, redirect
from .helper_functions import result_page, create_clearing_message, send_text_email

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from AccountingApp.models import *
from .core_algorithm import calculate_result, simple_result, is_room_cleared, related_result

import json


def sort_dict_by_values(d, reverse=False):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1][0], reverse=reverse)}


def simplify_dict(d):
    all_persons = []
    for k in d.keys():
        p_1, _, p_2 = k.split()
        if p_1 not in all_persons:
            all_persons.append(p_1)
        if p_2 not in all_persons:
            all_persons.append(p_2)
    
    getter_scores = {p: 0 for p in all_persons}
    giver_scores = {p: 0 for p in all_persons}
    
    for k in d.keys():
        if int(d[k][0]) > 0:
            p_1, _, p_2 = k.split()
            giver_scores[p_1] = giver_scores[p_1]+1
            getter_scores[p_2] = getter_scores[p_2]+1
    
    getters = []
    givers = []
    
    for getter in getter_scores:
        for giver in giver_scores:
            if getter_scores[getter] > 0 and giver_scores[giver] > 0 and getter == giver:
                must_be_getter = getter_scores[getter] > giver_scores[giver]
                if must_be_getter:
                    getters.append(getter)
                else:
                    givers.append(giver)
    
    to_simplify = []
    
    for k in d.keys():
        p_1, _, p_2 = k.split()
        item = f'{k}: {d[k][0]}'
        not_duplicate = item not in to_simplify
        not_zero = int(d[k][0]) > 0
        if p_1 in getters and not_duplicate and not_zero:
            to_simplify.append(f'{k}: {d[k][0]}')
        elif p_2 in givers and not_duplicate and not_zero:
            to_simplify.append(f'{k}: {d[k][0]}')
    
    
    print('\n###############################')
    print('TO_SIMPLIFY:')
    for i in to_simplify:
        print(i)
    if len(to_simplify) == 0:
        print('Nothing :)')
    print('###############################\n')
    
    return d


def print_sum_of_all_in_cmd(d):
    sum_of_all = {}
    for k, v in d.items():
        p_1, _, p_2 = k.split()
        v = int(v[0])
        if p_1 not in sum_of_all:
            sum_of_all[p_1] = -v
        else:
            sum_of_all[p_1] -= v
        if p_2 not in sum_of_all:
            sum_of_all[p_2] = v
        else:
            sum_of_all[p_2] += v
    sum_of_all = {k: v for k, v in sorted(sum_of_all.items(), key=lambda item: abs(item[1]), reverse=True)}
    
    print('###############################')
    print('KOLLAN_BEDEHKAR:')
    for k, v in sum_of_all.items():
        if v < 0:
            print(k, ':', -v)
    print()
    print('KOLLAN_TALABKAR:')
    for k, v in sum_of_all.items():
        if v > 0:
            print(k, ':', v)
    print('###############################\n')


def pretty_print(d):
    p = json.dumps(d, sort_keys=True, indent=4)
    print(p)


class DictOfSets(dict):
    
    def __setitem__(self, key, value):
        value_type = type(value).__name__
        if value_type != 'set':
            value = {value}
            
        dict.__setitem__(self, key, value)
    
    
    def __getitem__(self, key):
        if key not in list(self.keys()):
            self[key] = set({})
        return super().__getitem__(key)


def report_for_clearing(request, room_id):
    if request.user.is_anonymous:
        return result_page(request, "Please sign in")

    room = Room.objects.get(id=room_id)
    if room not in request.user.room_set.all():
        return result_page(request, "You're not the owner of the room")

    # The core algorithm:
    final_dict = calculate_result(room)
    cleared = is_room_cleared(final_dict)

    borders = [item.split(' --> ') for item in list(final_dict.keys()) if final_dict[item] != 0]
    zero_borders = []
    for b in borders:
        if final_dict[' --> '.join(b)][0] == 0:
            zero_borders.append(b)
    
    neighbours = DictOfSets()
    #TODO: detect way
    #TODO: detect cycle
    
    simplified_dict = simplify_dict(final_dict)
    print_sum_of_all_in_cmd(simplified_dict)
    sorted_final_dict = sort_dict_by_values(simplified_dict, reverse=True)
    context = {'result': sorted_final_dict, 'mode': 'report_for_clearing', 'room_name': room.name, 'cleared': cleared}
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
