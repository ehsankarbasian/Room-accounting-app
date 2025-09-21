from django.urls import path

from apps.ReportApp.views import HomeView, FinalReportAPI, ReportEmailView
from apps.ReportApp.views import FinalReportView, SpendListView, TransactionListView, RoomLogView
from apps.ReportApp.apps import ReportAppConfig

# Auto-generate app_name from AppConfig.name to handle optional 'apps.' prefix
app_name = ReportAppConfig.name.split('.')[-1]


urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    
    path('rooms/<int:room_id>/spends', SpendListView.as_view(), name='get_spends'),
    path('rooms/<int:room_id>/transactions', TransactionListView.as_view(), name='all_transactions'),
    path('rooms/<int:room_id>/log', RoomLogView.as_view(), name='room_log'),
    path('rooms/<int:room_id>/report', FinalReportView.as_view(), name='room_report'),
    
    path('reportForClearingAPI', FinalReportAPI.as_view()),
    path('send_report_email', ReportEmailView.as_view(), name='send_report_email'),
]
