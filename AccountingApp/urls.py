from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
]

auth_urls = [
    path('signin', sign_in),
    path('signup', sign_up),
    path('logout', log_out),

    path('forgotPassword', forgot_password),
    path('resetPasswordTokenBased', reset_password_token_based),
]

user_functions = [
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

result_functions = [
    path('reportForClearing/<int:room_id>', report_for_clearing),
    path('reportForClearingAPI', report_for_clearing_API),
    path('sendResultEmail', send_result_email),
]


pack_list = [
    auth_urls,
    user_functions,
    result_functions
]

for pack in pack_list:
    for url in pack:
        urlpatterns.append(url)
