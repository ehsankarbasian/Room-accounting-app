from django.contrib import admin
from .models import *


class RoomInLine(admin.TabularInline):
    model = Room


class PersonInLine(admin.TabularInline):
    model = Person
    fields = ('name', 'phone', 'email')


class SpendInLine(admin.TabularInline):
    model = Spend


class SpendersInLine(admin.TabularInline):
    model = Spenders


class PartnersInLine(admin.TabularInline):
    model = Partners


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


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['verify_email_code', 'user', 'verify_email_token']
    fields = [('verify_email_code', 'verify_email_token')]
    readonly_fields = ['verify_email_token']
    search_fields = ['user__username']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'created_at']
    fields = ['name', ('creator', 'created_at')]
    readonly_fields = ['creator', 'created_at']
    search_fields = ['creator__username']
    inlines = [PersonInLine, SpendInLine]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'room', 'verified_email', 'verified_phone']
    fields = ['name', 'room', ('email', 'phone')]
    readonly_fields = ['name', 'email', 'phone', 'room']
    search_fields = ['room__creator__username']


@admin.register(Transaction)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['amount', 'payer', 'receiver', 'date']
    fields = ['amount', ('payer', 'receiver'), 'date']
    readonly_fields = ['amount', 'payer', 'receiver', 'date']
    search_fields = ['payer__room__creator__username']


@admin.register(Spend)
class SpendAdmin(admin.ModelAdmin):
    list_display = ['amount', 'description','room', 'date']
    list_editable = ['description']
    fields = ['amount', 'room', 'description']
    readonly_fields = ['amount', 'room', 'description']
    search_fields = ['room__creator__username']
    inlines = [SpendersInLine, PartnersInLine]


@admin.register(Spenders)
class SpendersAdmin(admin.ModelAdmin):
    list_display = ['weight', 'spender_person', 'spender_spend']
    fields = ['weight', 'spender_person', 'spender_spend']
    readonly_fields = ['spender_person', 'spender_spend']
    search_fields = ['spender_person__username']


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ['weight', 'partner_person', 'partner_spend']
    fields = ['weight', 'partner_person', 'partner_spend']
    readonly_fields = ['partner_person', 'partner_spend']
    search_fields = ['partner_person__username']
