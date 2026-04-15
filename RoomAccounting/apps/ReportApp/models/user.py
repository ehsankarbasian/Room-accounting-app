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


class Token(models.Model):
    verify_email_token = models.CharField(max_length=64, null=True)
    verify_email_code = models.IntegerField(null=True)

    reset_pass_token = models.CharField(max_length=64, null=True)
    reset_pass_code = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = verbose_name_plural('Tokens')

    def __str__(self):
        return "Tokens of: " + self.user.username
