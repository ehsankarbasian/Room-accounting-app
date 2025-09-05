from django.urls import path

from ReportApp.views import HomeView, FinalReportView, FinalReportAPI, ReportEmailView
from ReportApp.apps import ReportAppConfig

app_name = ReportAppConfig.name


urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('rooms/<int:room_id>/report', FinalReportView.as_view(), name='room_report'),
    
    path('reportForClearingAPI', FinalReportAPI.as_view()),
    path('send_report_email', ReportEmailView.as_view(), name='send_report_email'),
]
