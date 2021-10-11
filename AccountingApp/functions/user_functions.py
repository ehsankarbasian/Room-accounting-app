from itertools import chain

from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from AccountingApp.models import *
from .helper_functions import result_page


def add_room(request):
    room_name = request.GET['room_name']

    if request.user.is_authenticated:
        Room.objects.create(name=room_name, creator=request.user)
        return redirect('home')
    return result_page(request, "Please sign in.")


def delete_room(request, room_id):
    if request.user.is_anonymous:
        return result_page(request, "Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        room.delete()
        return redirect('home')
    return result_page(request, "You're not the owner of the room")


@require_http_methods(["POST"])
def edit_room(request, room_id):
    if request.user.is_anonymous:
        return result_page(request, "Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        room.name = request.POST['room_name']
        room.save()
        return redirect('home')
    return result_page(request, "You're not the owner of the room")


@require_http_methods(["POST"])
def add_person(request, room_id):
    if request.user.is_anonymous:
        return result_page(request, "Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        name = request.POST['person_name']
        email = request.POST['email']
        phone = request.POST['phone']
        Person.objects.create(name=name, email=email, phone=phone, room=room)
        return redirect('home')
    return result_page(request, "You're not the owner of the room")


@require_http_methods(["POST"])
def add_buy(request, room_id):
    if request.user.is_anonymous:
        return result_page(request, "Please sign in")

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
                # TODO: get and save weight
                Spenders.objects.create(spender_person=person, spender_spend=spend)

            # Create Partners
            if "partner"+ID in request.POST:
                # TODO: get and save weight
                Partners.objects.create(partner_person=person, partner_spend=spend)

        return redirect('home')

    return result_page(request, "You're not the owner of the room")


def all_buys(request, room_id):
    if request.user.is_anonymous:
        return result_page(request, "Please sign in")

    room = Room.objects.get(id=room_id)
    if room in request.user.room_set.all():
        spends = room.spend_set.all().order_by('-date')

        context = {'spends': spends, 'mode': 'spend_log', 'room_name': room.name}
        return render(request, 'log.html', context=context)

    return result_page(request, "You're not the owner of the room")


@require_http_methods(["POST"])
def add_transaction(request, room_id):
    if request.user.is_anonymous:
        return result_page(request, "Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        amount = request.POST['amount']
        payer_id = request.POST['Payer']
        receiver_id = request.POST['Receiver']

        if payer_id == receiver_id:
            return result_page(request, "ERROR: The payer and the receiver are the same")

        payer = Person.objects.get(id=payer_id)
        receiver = Person.objects.get(id=receiver_id)
        Transaction.objects.create(amount=amount, payer=payer, receiver=receiver)
        return redirect('home')

    return result_page(request, "You're not the owner of the room")


def all_transactions(request, room_id):
    if request.user.is_anonymous:
        return result_page(request, "Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        persons = room.person_set.all()
        payer_query = Q(payer__in=persons)
        receiver_query = Q(receiver__in=persons)
        transactions = Transaction.objects.filter(payer_query | receiver_query).order_by('-date')

        context = {'transactions': transactions, 'mode': 'transaction_log', 'room_name': room.name}
        return render(request, 'log.html', context=context)

    return result_page(request, "You're not the owner of the room")


def room_log(request, room_id):
    if request.user.is_anonymous:
        return result_page(request, "Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        transactions = room.transaction_set
        spends = room.spend_set.all().order_by('-date')

        log = sorted(chain(transactions, spends),
                     key=lambda item: item.date,
                     reverse=True)

        context = {'log': log, 'mode': 'room_log', 'room_name': room.name}
        return render(request, 'log.html', context=context)

    return result_page(request, "You're not the owner of the room")
