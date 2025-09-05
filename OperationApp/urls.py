from django.urls import path

from OperationApp.views import AddRoomView, DeleteRoomView, EditRoomView, AddPersonView, AddSpendView, AddTransactionView, SpendListView, TransactionListView, RoomLogView
from OperationApp.apps import OperationAppConfig

app_name = OperationAppConfig.name


urlpatterns = [
    path('rooms/add', AddRoomView.as_view(), name='add_room'),
    path('rooms/<int:room_id>/delete_room', DeleteRoomView.as_view(), name='delete_room'),
    path('rooms/<int:room_id>/edit_room', EditRoomView.as_view(), name='edit_room'),

    path('rooms/<int:room_id>/add/person', AddPersonView.as_view(), name='add_person'),
    path('rooms/<int:room_id>/add/spend', AddSpendView.as_view(), name='add_spend'),
    path('rooms/<int:room_id>/add/transaction', AddTransactionView.as_view(), name='add_transaction'),

    path('rooms/<int:room_id>/spends', SpendListView.as_view(), name='get_spends'),
    path('rooms/<int:room_id>/transactions', TransactionListView.as_view(), name='all_transactions'),
    path('rooms/<int:room_id>/log', RoomLogView.as_view(), name='room_log'),
]
