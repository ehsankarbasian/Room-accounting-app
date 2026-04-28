from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.ReportApp.models._base import verbose_name_plural


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=20, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True)

    verified_email = models.BooleanField(default=False)
    verified_phone = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = verbose_name_plural('Users')

    def __str__(self):
        return self.username + " (room_count:" + str(self.room_set.count()) + ")"
