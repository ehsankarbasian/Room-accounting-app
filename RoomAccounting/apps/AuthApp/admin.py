from django.apps import apps
from django.contrib import admin

from apps.AuthApp.models import User
Room = apps.get_model('ReportApp', 'Room')


class RoomInLine(admin.TabularInline):
    model = Room
    fk_name = "creator"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    list_display = ['username', 'email', 'verified_email', 'verified_phone', 'fullname', 'phone_number']
    list_editable = ['verified_email', 'verified_phone']
    list_filter = ['verified_email', 'verified_phone']
    search_fields = ['username', 'email']
    fieldsets = (
        ('General Info', {
            'fields': ('username',
                       ('email', 'phone_number'))
        }),
        ('More info', {
            'fields': (('verified_email', 'verified_phone', 'fullname'),
                       ('date_joined', 'last_login'),
                       ('is_staff', 'is_superuser'))
        })
    )
    readonly_fields = ['username', 'email', 'date_joined', 'last_login', 'is_staff', 'is_superuser']
    inlines = [RoomInLine]
