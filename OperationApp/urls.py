from django.urls import path

from OperationApp.views import AddRoomView, DeleteRoomView, EditRoomView, AddPersonView, AddSpendView, AddTransactionView, SpendListView, TransactionListView, RoomLogView


urlpatterns = [
    path('addRoom', AddRoomView.as_view()),
    path('deleteRoom/<int:room_id>', DeleteRoomView.as_view()),
    path('editRoom/<int:room_id>', EditRoomView.as_view()),

    path('addPerson/<int:room_id>', AddPersonView.as_view()),
    path('addBuy/<int:room_id>', AddSpendView.as_view()),
    path('addTransaction/<int:room_id>', AddTransactionView.as_view()),

    path('allBuys/<int:room_id>', SpendListView.as_view()),
    path('allTransactions/<int:room_id>', TransactionListView.as_view()),
    path('roomLog/<int:room_id>', RoomLogView.as_view()),
]
