from django.contrib.auth import authenticate
from django.contrib.auth import login

from django.shortcuts import render
from django.http.response import HttpResponse

from .models import User

from RoomAccounting.settings import HOST, PORT


def landing_page(request):
    context = {'HOST': HOST, 'PORT': PORT}
    return render(request, 'index.html', context=context)


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
        return HttpResponse('Login completed successfully')

    return HttpResponse('Please login with post method')
