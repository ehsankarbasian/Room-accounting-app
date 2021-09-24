from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True)


class Room(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, default="new_room")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class Spend(models.Model):
    amount = models.IntegerField(default=0)
    description = models.CharField(max_length=256, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    spenders = models.ForeignKey("Spenders", on_delete=models.DO_NOTHING)
    partners = models.ForeignKey("Partners", on_delete=models.DO_NOTHING)


class Spenders(models.Model):
    weight = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'spender (Person m2m Spend)'


class Partners(models.Model):
    weight = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'partner (Person m2m Spend)'


class Person(models.Model):
    name = models.CharField(max_length=100, default="new_person")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    spenders = models.ForeignKey("Spenders", on_delete=models.DO_NOTHING)
    partners = models.ForeignKey("Partners", on_delete=models.DO_NOTHING)


class Transaction(models.Model):
    payer = models.ForeignKey("Person", related_name="payer", on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey("Person", related_name="receiver", on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)
