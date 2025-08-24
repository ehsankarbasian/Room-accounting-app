from django.urls import path

from AuthApp.views import sign_in, sign_up, log_out, forgot_password, reset_password_token_based


urlpatterns = [
    path('signin', sign_in),
    path('signup', sign_up),
    path('logout', log_out),

    path('forgotPassword', forgot_password),
    path('resetPasswordTokenBased', reset_password_token_based),
]
