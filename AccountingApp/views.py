from django.contrib.auth import authenticate
from django.contrib.auth import login

from django.shortcuts import render, redirect
from django.http.response import HttpResponse

from .models import User, Room, Person, Spend, Spenders, Partners

from RoomAccounting.settings import HOST, PORT


def landing_page(request):
    context = {'HOST': HOST, 'PORT': PORT}
    return render(request, 'index.html', context=context)


def home(request):
    user = request.user
    rooms = Room.objects.filter(creator=user)[::-1]
    context = {'HOST': HOST, 'PORT': PORT, 'username': user.username, 'rooms': rooms}
    return render(request, 'home.html', context=context)


def sign_up(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(username=username,
                                 password=password,
                                 email=email,
                                 fullname=fullname)
        return HttpResponse("Signed up successfully, now sign in please")

    return HttpResponse('Please signup with post method')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponse('Wrong username/password')

        login(request, user)
        return redirect('home')

    return HttpResponse('Please login with post method')


def logout(request):
    request.user = None
    return redirect('landing_page')


def add_room(request):
    if request.method == 'GET':
        room_name = request.GET['room_name']

        if request.user.is_authenticated:
            Room.objects.create(name=room_name, creator=request.user)
            return redirect('home')
        return HttpResponse('Please signIn')

    return HttpResponse('Please add room with get method')


def delete_room(request, room_id):
    Room.objects.get(id=room_id).delete()
    return redirect('home')


def edit_room(request, room_id):
    if request.method == 'POST':
        room = Room.objects.get(id=room_id)

        if room in request.user.room_set.all():
            room.name = request.POST['room_name']
            room.save()
            return redirect('home')

        return HttpResponse("You're not the owner of the room")

    return HttpResponse("please use POST method")


def add_person(request, room_id):
    if request.method == 'POST':
        room = Room.objects.get(id=room_id)

        if room in request.user.room_set.all():
            name = request.POST['person_name']
            Person.objects.create(name=name,
                                  room=room)
            return redirect('home')

        return HttpResponse("You're not the owner of the room")

    return HttpResponse("please use POST method")


def add_buy(request, room_id):
    if request.method == 'POST':
        room = Room.objects.get(id=room_id)

        if room in request.user.room_set.all():
            amount = request.POST['amount']
            description = request.POST['amount']
            spend = Spend.objects.create(amount=amount,
                                         description=description,
                                         room=room)
            person_set = room.person_set.all()

            for person in person_set:
                # Create Spenders
                ID = str(person.id)
                if "spender"+ID in request.POST:
                    Spenders.objects.create(spender_person=person,
                                            spender_spend=spend) # TODO: weight

                # Create Partners
                if "partner"+ID in request.POST:
                    Partners.objects.create(partner_person=person,
                                            partner_spend=spend) # TODO: weight

            return redirect('home')

        return HttpResponse("You're not the owner of the room")

    return HttpResponse("please use POST method")
