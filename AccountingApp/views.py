from .functions.auth_functions import *
from .functions.core_algorithm import cleared_person
from .functions.user_functions import *
from .functions.result_functions import *


def landing_page(request):
    if not request.user.is_anonymous:
        return home(request)

    context = {'HOST': HOST, 'PORT': PORT, 'app_base_url': ROOM_ACCOUNTING_APP_BASE_URL}
    return render(request, 'index.html', context=context)


def home(request):
    user = request.user
    rooms = Room.objects.filter(creator=user).order_by("created_at")
    context = {'HOST': HOST, 'PORT': PORT, 'app_base_url': ROOM_ACCOUNTING_APP_BASE_URL,
               'username': user.username, 'rooms': rooms, 'cleared_person': cleared_person}
    return render(request, 'home.html', context=context)
