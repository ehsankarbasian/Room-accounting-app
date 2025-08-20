from django.shortcuts import render

from AccountingApp.models import Room
from RoomAccounting.settings import HOST, PORT, ROOM_ACCOUNTING_APP_BASE_URL


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
