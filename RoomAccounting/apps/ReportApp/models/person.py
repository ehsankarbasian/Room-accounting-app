from django.db import models
from django.db.models import Q

from apps.ReportApp.models._base import verbose_name_plural

from apps.ReportApp.models import Transaction, Spend


class Person(models.Model):
    name = models.CharField(max_length=100, default="new_person")
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=False)
    room = models.ForeignKey("Room", on_delete=models.CASCADE)

    verify_email_token = models.CharField(max_length=64)
    verify_phone_code = models.IntegerField()

    cleared = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = verbose_name_plural('Persons')

    @property
    def related_transactions(self):
        query = Q(payer=self) | Q(receiver=self)
        return Transaction.objects.filter(query)

    @property
    def related_spends(self):
        related_id = []
        for spend in Spend.objects.filter(room=self.room):
            union_spenders = self.spenders_set.filter(id__in=spend.spenders_set.values_list('id', flat=True))
            union_partners = self.partners_set.filter(id__in=spend.partners_set.values_list('id', flat=True))
            if union_spenders.count() or union_partners.count():
                related_id.append(spend.id)
        return Spend.objects.filter(id__in=related_id)

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
