from django.urls import path

from ReportApp.views import HomeView, FinalReportView, FinalReportAPI
from ReportApp.apps import ReportAppConfig

app_name = ReportAppConfig.name


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('reportForClearing/<int:room_id>', FinalReportView.as_view()),
    path('reportForClearingAPI', FinalReportAPI.as_view()),
    # path('sendResultEmail', send_result_email),
]
