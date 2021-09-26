from django.urls import path
from .views import *

urlpatterns = [
    path('signin', signIn),
    path('signup', signUp),
    path('logout', logout),

    path('', home, name='home'),
    path('addRoom', addRoom)
]
