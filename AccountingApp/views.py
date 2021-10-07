from itertools import chain

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

from .models import *
from RoomAccounting.settings import HOST, PORT


def landing_page(request):
    if not request.user.is_anonymous:
        return home(request)

    context = {'HOST': HOST, 'PORT': PORT}
    return render(request, 'index.html', context=context)


def home(request):
    user = request.user
    rooms = Room.objects.filter(creator=user).order_by("-created_at")
    context = {'HOST': HOST, 'PORT': PORT, 'username': user.username, 'rooms': rooms}
    return render(request, 'home.html', context=context)


@require_http_methods(["POST"])
def sign_up(request):
    fullname = request.POST['fullname']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    User.objects.create_user(username=username,
                             password=password,
                             email=email,
                             fullname=fullname)
    return HttpResponse("Signed up successfully, now sign in please")


@require_http_methods(["POST"])
def sign_in(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponse('Wrong username/password')

    login(request, user)
    return redirect('home')


def log_out(request):
    logout(request)
    return redirect('landing_page')


def add_room(request):
    room_name = request.GET['room_name']

    if request.user.is_authenticated:
        Room.objects.create(name=room_name, creator=request.user)
        return redirect('home')
    return HttpResponse('Please signIn')


def delete_room(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        room.delete()
        return redirect('home')
    return HttpResponse("You're not the owner of the room")


@require_http_methods(["POST"])
def edit_room(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        room.name = request.POST['room_name']
        room.save()
        return redirect('home')
    return HttpResponse("You're not the owner of the room")


@require_http_methods(["POST"])
def add_person(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        name = request.POST['person_name']
        Person.objects.create(name=name, room=room)
        return redirect('home')
    return HttpResponse("You're not the owner of the room")


@require_http_methods(["POST"])
def add_buy(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        amount = request.POST['amount']
        description = request.POST['description']
        spend = Spend.objects.create(amount=amount, description=description, room=room)

        # m2m relationships:
        for person in room.person_set.all():
            # Create Spenders
            ID = str(person.id)
            if "spender"+ID in request.POST:
                # TODO: det and save weight
                Spenders.objects.create(spender_person=person, spender_spend=spend)

            # Create Partners
            if "partner"+ID in request.POST:
                # TODO: det and save weight
                Partners.objects.create(partner_person=person, partner_spend=spend)

        return redirect('home')

    return HttpResponse("You're not the owner of the room")


def all_buys(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)
    if room in request.user.room_set.all():
        spends = room.spend_set.all().order_by('-date')

        context = {'spends': spends, 'mode': 'spend_log', 'room_name': room.name}
        return render(request, 'log.html', context=context)

    return HttpResponse("You're not the owner of the room")


@require_http_methods(["POST"])
def add_transaction(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        amount = request.POST['amount']
        payer_id = request.POST['Payer']
        receiver_id = request.POST['Receiver']

        if payer_id == receiver_id:
            return HttpResponse('ERROR: The payer and the receiver are the same')

        payer = Person.objects.get(id=payer_id)
        receiver = Person.objects.get(id=receiver_id)
        Transaction.objects.create(amount=amount, payer=payer, receiver=receiver)
        return redirect('home')

    return HttpResponse("You're not the owner of the room")


def all_transactions(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        persons = room.person_set.all()
        payer_query = Q(payer__in=persons)
        receiver_query = Q(receiver__in=persons)
        transactions = Transaction.objects.filter(payer_query | receiver_query).order_by('-date')

        context = {'transactions': transactions, 'mode': 'transaction_log', 'room_name': room.name}
        return render(request, 'log.html', context=context)

    return HttpResponse("You're not the owner of the room")


def room_log(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        transactions = room.transaction_set
        spends = room.spend_set.all().order_by('-date')

        log = sorted(chain(transactions, spends),
                     key=lambda item: item.date,
                     reverse=True)

        context = {'log': log, 'mode': 'room_log', 'room_name': room.name}
        return render(request, 'log.html', context=context)

    return HttpResponse("You're not the owner of the room")


def report_for_clearing(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)
    if room not in request.user.room_set.all():
        return HttpResponse("You're not the owner of the room")

    # The core algorithm:
    final_dict = calculate_result(room)

    result = []
    for k, v in final_dict.items():
        result.append(k+": "+str(v))
    return render(request, 'result.html', context={'result': result})


def calculate_result(room):
    persons = list(room.person_set.all())

    result_dict = dict({})
    max_index = len(persons) - 1
    for p1 in persons:
        p1_index = persons.index(p1)
        if p1_index < max_index:
            remaining_persons = persons[p1_index + 1:]
            for p2 in remaining_persons:
                result_dict[str(p1.id) + '  ---->  ' + str(p2.id)] = 0

    spends_list = []
    for spend in room.spend_set.all():
        amount = spend.amount

        partner_dict = spend.partner_dict()
        partners_sum_of_weight = 0
        for k, v in partner_dict.items():
            partners_sum_of_weight += partner_dict[k]
        # part_of_each_partner_weight = [amount / partners_sum_of_weight if partners_sum_of_weight else 0][0]

        spender_dict = spend.spender_dict()
        spenders_sum_of_weight = 0
        for k in spender_dict:
            spenders_sum_of_weight += spender_dict[k]
        # part_of_each_spender_weight = [amount / spenders_sum_of_weight if spenders_sum_of_weight else 0][0]

        the_spent = {'amount': amount,
                     'partner_dict': partner_dict,
                     'spender_dict': spender_dict,
                     # 'part_of_each_partner_weight': part_of_each_partner_weight,
                     # 'part_of_each_spender_weight': part_of_each_spender_weight
                     }

        spends_list.append(the_spent)

    # result_dict complement:
    for spend in spends_list:
        amount = spend['amount']
        spender_dict = spend['spender_dict']
        # part_of_each_spender_weight = spend['part_of_each_spender_weight']
        partner_dict = spend['partner_dict']
        # part_of_each_partner_weight = spend['part_of_each_partner_weight']

        partners_sum_of_weight = 0
        spenders_sum_of_weight = 0
        for k, v in partner_dict.items():
            partners_sum_of_weight += partner_dict[k]
        for k, v in spender_dict.items():
            spenders_sum_of_weight += spender_dict[k]

        for k, v in result_dict.items():
            if spender_dict[int(k.split()[0])] and partner_dict[int(k.split()[2])]:
                result_dict[k] -= amount * partner_dict[int(k.split()[2])] / partners_sum_of_weight\
                                  * spender_dict[int(k.split()[0])] / spenders_sum_of_weight

            if partner_dict[int(k.split()[0])] and spender_dict[int(k.split()[2])]:
                result_dict[k] += amount * partner_dict[int(k.split()[2])] / partners_sum_of_weight\
                                  * spender_dict[int(k.split()[0])] / spenders_sum_of_weight

    transactions = room.transaction_set
    for transaction in transactions:
        payer_id = transaction.payer.id
        receiver_id = transaction.receiver.id
        amount = transaction.amount
        for k, v in result_dict.items():
            if payer_id == int(k.split()[0]) and receiver_id == int(k.split()[2]):
                result_dict[k] -= amount
            elif payer_id == int(k.split()[2]) and receiver_id == int(k.split()[0]):
                result_dict[k] += amount

    final_dict = {}
    for k, v in result_dict.items():
        key_lst = k.split()
        if v < 0:
            key_lst = key_lst[::-1]
        key = key_lst[0] + ' ' + key_lst[1] + ' ' + key_lst[2]
        final_dict[key] = int(abs(v))

    return final_dict
