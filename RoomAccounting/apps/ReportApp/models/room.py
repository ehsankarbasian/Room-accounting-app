from django.db import models
from django.db.models import Q

from apps.ReportApp.models._base import verbose_name_plural

from apps.ReportApp.models import Transaction


class Room(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, default="new_room")
    creator = models.ForeignKey("User", on_delete=models.CASCADE, null=True)

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
