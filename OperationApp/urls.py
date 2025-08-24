from django.urls import path

from OperationApp.views import add_room, delete_room, edit_room, add_person, add_buy, add_transaction, all_buys, all_transactions, room_log


urlpatterns = [
    path('addRoom', add_room),
    path('deleteRoom/<int:room_id>', delete_room),
    path('editRoom/<int:room_id>', edit_room),

    path('addPerson/<int:room_id>', add_person),
    path('addBuy/<int:room_id>', add_buy),
    path('addTransaction/<int:room_id>', add_transaction),

    path('allBuys/<int:room_id>', all_buys),
    path('allTransactions/<int:room_id>', all_transactions),
    path('roomLog/<int:room_id>', room_log),
]
