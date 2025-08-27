from django.urls import path

from OperationApp.views import AddRoomView, DeleteRoomView, EditRoomView, AddPersonView, AddSpendView, AddTransactionView, SpendListView, TransactionListView, RoomLogView
from OperationApp.apps import OperationAppConfig

app_name = OperationAppConfig.name


urlpatterns = [
    path('add_room', AddRoomView.as_view(), name='add_room'),
    path('delete_room/<int:room_id>', DeleteRoomView.as_view(), name='delete_room'),
    path('edit_room/<int:room_id>', EditRoomView.as_view(), name='edit_room'),

    path('add_person/<int:room_id>', AddPersonView.as_view(), name='add_person'),
    path('add_spend/<int:room_id>', AddSpendView.as_view(), name='add_spend'),
    path('add_transaction/<int:room_id>', AddTransactionView.as_view(), name='add_transaction'),

    path('get_spends/<int:room_id>', SpendListView.as_view(), name='get_spends'),
    path('all_transactions/<int:room_id>', TransactionListView.as_view(), name='all_transactions'),
    path('room_log/<int:room_id>', RoomLogView.as_view(), name='room_log'),
]
