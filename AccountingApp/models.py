from secrets import token_hex
from random import randint

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from RoomAccounting.settings import ADMIN_PRIORITY


def verbose_name_plural(model_name):
    for model in ADMIN_PRIORITY:
        if model_name in model:
            return ' ' * ADMIN_PRIORITY[::-1].index(model_name) + model_name
    return 'ERROR: TABLE NAME NOT FOUND IN settings'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=20, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True)

    verified_email = models.BooleanField(default=False)
    verified_phone = models.BooleanField(default=False)
    token = models.OneToOneField("Token", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = verbose_name_plural('Users')

    def __str__(self):
        return self.username + " (room_count:" + str(self.room_set.count()) + ")"


class Token(models.Model):
    verify_email_token = models.CharField(max_length=64, null=True)
    verify_email_code = models.IntegerField(null=True)

    reset_pass_token = models.CharField(max_length=64, default=token_hex(64))
    reset_pass_code = models.IntegerField(default=randint(100000, 999999))

    class Meta:
        verbose_name_plural = verbose_name_plural('Tokens')

    def __str__(self):
        return "Tokens of: " + self.user.username


class Room(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, default="new_room")
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = verbose_name_plural('Rooms')

    @property
    def transaction_set(self):
        persons = self.person_set.all()
        payer_query = Q(payer__in=persons)
        receiver_query = Q(receiver__in=persons)
        return Transaction.objects.filter(payer_query | receiver_query).order_by('-date')

    def __str__(self):
        return self.name + " (creator: " + self.creator.username + ")"


class Spend(models.Model):
    amount = models.IntegerField(default=0)
    description = models.CharField(max_length=256, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name_plural('Spends')

    def partner_dict(self):
        result = dict({})
        room = self.room

        for person in room.person_set.all():
            result[person.id] = 0
        for partner in self.partners_set.all():
            result[partner.partner_person.id] = partner.weight

        return result

    def spender_dict(self):
        result = dict({})
        room = self.room

        for person in room.person_set.all():
            result[person.id] = 0
        for spender in self.spenders_set.all():
            result[spender.spender_person.id] = spender.weight

        return result

    @property
    def is_transaction(self):
        return False

    def __str__(self):
        return str(self.amount) + " for " + self.description + " (room:" + self.room.name + ")"


class Spenders(models.Model):
    weight = models.IntegerField(default=1)
    spender_person = models.ForeignKey("Person", on_delete=models.DO_NOTHING, default=None)
    spender_spend = models.ForeignKey("Spend", on_delete=models.DO_NOTHING, default=None)

    class Meta:
        verbose_name_plural = verbose_name_plural('spender (Person m2m Spend)')

    def __str__(self):
        return "spender " + str(self.spender_person.id) + " <--> " + str(self.spender_spend.id) + " spend"


class Partners(models.Model):
    weight = models.IntegerField(default=1)
    partner_person = models.ForeignKey("Person", on_delete=models.DO_NOTHING, default=None)
    partner_spend = models.ForeignKey("Spend", on_delete=models.DO_NOTHING, default=None)

    class Meta:
        verbose_name_plural = verbose_name_plural('partner (Person m2m Spend)')

    def __str__(self):
        return "partner " + str(self.partner_person.id) + " <--> " + str(self.partner_spend.id) + " spend"


class Person(models.Model):
    name = models.CharField(max_length=100, default="new_person")
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    verify_email_token = models.CharField(max_length=64, default=token_hex(64))
    verify_phone_code = models.IntegerField(default=randint(100000, 999999))

    class Meta:
        verbose_name_plural = verbose_name_plural('Persons')

    @property
    def verified_email(self):
        return self.verify_email_token == "verified email"

    def verify_email(self):
        self.verify_email_token = "verified email"
        self.save()

    @property
    def verified_phone(self):
        return self.verify_phone_code == 0

    def verify_phone(self):
        self.verify_phone_code = 0
        self.save()

    def __str__(self):
        return self.name + " (room: " + self.room.name + ")"


class Transaction(models.Model):
    payer = models.ForeignKey("Person", related_name="payer", on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey("Person", related_name="receiver", on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = verbose_name_plural('Transactions')

    @property
    def is_transaction(self):
        return True

    def __str__(self):
        return str(self.amount) + " from " + self.payer.name + " to " + self.receiver.name\
               + " (room:" + self.payer.room.name + ")"
