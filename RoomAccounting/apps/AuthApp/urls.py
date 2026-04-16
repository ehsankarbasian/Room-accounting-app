from django.urls import path

from apps.AuthApp.views import SignUpView, SignInView, LogOutView
from apps.AuthApp.apps import AuthAppConfig

# Auto-generate app_name from AppConfig.name to handle optional 'apps.' prefix
app_name = AuthAppConfig.name.split('.')[-1]


urlpatterns = [
    path('sign_up', SignUpView.as_view(), name='sign_up'),
    path('sign_in', SignInView.as_view(), name='sign_in'),
    path('logout', LogOutView.as_view(), name='logout'),
]
