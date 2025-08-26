from django.urls import path

from ReportApp.views import HomeView, FinalReportView, FinalReportAPI
from ReportApp.apps import ReportAppConfig

app_name = ReportAppConfig.name


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('room_final_report/<int:room_id>', FinalReportView.as_view(), name='room_final_report'),
    
    path('reportForClearingAPI', FinalReportAPI.as_view()),
    # path('sendResultEmail', send_result_email),
]
