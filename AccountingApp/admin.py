from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Token)
admin.site.register(Room)
admin.site.register(Spend)
admin.site.register(Spenders)
admin.site.register(Partners)
admin.site.register(Person)
admin.site.register(Transaction)
