from django.contrib.auth import authenticate
from django.contrib.auth import login

from django.shortcuts import render, redirect
from django.http.response import HttpResponse

from .models import User, Room

from RoomAccounting.settings import HOST, PORT


def landing_page(request):
    context = {'HOST': HOST, 'PORT': PORT}
    return render(request, 'index.html', context=context)


def home(request):
    user = request.user
    rooms = Room.objects.filter(creator=user)
    context = {'HOST': HOST, 'PORT': PORT, 'username': user.username, 'rooms': rooms}
    return render(request, 'home.html', context=context)


def signUp(request):
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


def signIn(request):
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


def addRoom(request):
    if request.method == 'GET':
        room_name = request.GET['room_name']

        if request.user.is_authenticated:
            Room.objects.create(name=room_name, creator=request.user)
            return HttpResponse('Room created successfully')
        return HttpResponse('Please signIn')

    return HttpResponse('Please add room with get method')
