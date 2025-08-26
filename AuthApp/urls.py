from django.urls import path

from AuthApp.views import SignUpView, SignInView, LogOutView, ForgotPasswordView, ResetPasswordTokenBasedAPI
from AuthApp.apps import AuthAppConfig

app_name = AuthAppConfig.name


urlpatterns = [
    path('signup', SignUpView.as_view()),
    path('signin', SignInView.as_view()),
    path('logout', LogOutView.as_view()),

    path('forgotPassword', ForgotPasswordView.as_view()),
    path('resetPasswordTokenBased', ResetPasswordTokenBasedAPI.as_view()),
]
