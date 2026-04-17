from django.urls import path

from apps.AuthApp.views import SignUpView, SignInView, LogOutView
from apps.AuthApp.apps import AuthAppConfig

from apps.NotificationApp.contrib.features.feature_urls import (
    send_otp_path, verify_otp_path,
    send_forgot_password_message_path, reset_password_path,
)

# Auto-generate app_name from AppConfig.name to handle optional 'apps.' prefix
app_name = AuthAppConfig.name.split('.')[-1]


urlpatterns = [
    path('sign_up', SignUpView.as_view(), name='sign_up'),
    path('sign_in', SignInView.as_view(), name='sign_in'),
    path('logout', LogOutView.as_view(), name='logout'),
    
    send_otp_path(name='send_otp'),
    verify_otp_path(name='verify_otp'),
    
    send_forgot_password_message_path(name="forgot_password"),
    reset_password_path(name="reset_password"),
]
