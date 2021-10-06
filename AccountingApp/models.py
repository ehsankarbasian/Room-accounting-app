from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True)

    def __str__(self):
        name = [self.fullname if self.fullname else self.username][0]
        return name + " (room_count:" + str(self.room_set.count()) + ")"


class Room(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, default="new_room")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " (creator: " + self.creator.fullname + ")"


class Spend(models.Model):
    amount = models.IntegerField(default=0)
    description = models.CharField(max_length=256, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

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
        verbose_name_plural = 'spender (Person m2m Spend)'

    def __str__(self):
        return "spender " + str(self.spender_person.id) + " <--> " + str(self.spender_spend.id) + " spend"


class Partners(models.Model):
    weight = models.IntegerField(default=1)
    partner_person = models.ForeignKey("Person", on_delete=models.DO_NOTHING, default=None)
    partner_spend = models.ForeignKey("Spend", on_delete=models.DO_NOTHING, default=None)

    class Meta:
        verbose_name_plural = 'partner (Person m2m Spend)'

    def __str__(self):
        return "partner " + str(self.partner_person.id) + " <--> " + str(self.partner_spend.id) + " spend"


class Person(models.Model):
    name = models.CharField(max_length=100, default="new_person")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " (room:" + self.room.name + ")"


class Transaction(models.Model):
    payer = models.ForeignKey("Person", related_name="payer", on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey("Person", related_name="receiver", on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)

    @property
    def is_transaction(self):
        return True

    def __str__(self):
        return str(self.amount) + " from " + self.payer.name + " to " + self.receiver.name\
               + " (room:" + self.payer.room.name + ")"
