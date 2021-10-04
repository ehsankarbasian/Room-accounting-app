from django.urls import path
from .views import *

urlpatterns = [
    path('signin', sign_in),
    path('signup', sign_up),
    path('logout', logout),

    path('', home, name='home'),
    path('addRoom', add_room),

    path('deleteRoom/<int:room_id>', delete_room),
    path('editRoom/<int:room_id>', edit_room),
    path('addPerson/<int:room_id>', add_person),

    path('addBuy/<int:room_id>', add_buy),
    path('allBuys/<int:room_id>', all_buys),

    path('addTransaction/<int:room_id>', add_transaction),
    path('allTransactions/<int:room_id>', all_transactions),

    path('roomLog/<int:room_id>', room_log),
]
