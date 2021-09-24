from django.urls import path
from .views import *

urlpatterns = [
    path('signin', signIn),
    path('signup', signUp)
]
