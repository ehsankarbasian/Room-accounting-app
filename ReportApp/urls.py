from django.urls import path

from ReportApp.views import home, FinalReportView, FinalReportAPI


urlpatterns = [
    path('', home, name='home'),
    path('reportForClearing/<int:room_id>', FinalReportView.as_view()),
    path('reportForClearingAPI', FinalReportAPI.as_view()),
    # path('sendResultEmail', send_result_email),
]
