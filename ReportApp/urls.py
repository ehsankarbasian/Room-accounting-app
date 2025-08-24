from django.urls import path

from ReportApp.views import home, report_for_clearing, report_for_clearing_API


urlpatterns = [
    path('', home, name='home'),
    path('reportForClearing/<int:room_id>', report_for_clearing),
    path('reportForClearingAPI', report_for_clearing_API),
    # path('sendResultEmail', send_result_email),
]
