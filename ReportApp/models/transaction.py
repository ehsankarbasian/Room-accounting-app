from django.db import models
from django.db.models import Q

from ReportApp.models._base import verbose_name_plural

from ReportApp.models import Room


class TransactionQuerySet(models.QuerySet):
    
    def filter_by_room(self, room: Room):
        persons = room.person_set.all()
        payer_query = Q(payer__in=persons)
        receiver_query = Q(receiver__in=persons)
        return self.filter(payer_query | receiver_query)
    
    def select_related_payer_and_receiver(self):
        return self.select_related("payer", "receiver")


class TransactionManager(models.Manager):
    
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db)

    def filter_by_room(self, room: Room):
        return self.get_queryset().filter_by_room(room)
    
    def select_related_payer_and_receiver(self):
        return self.get_queryset().select_related_payer_and_receiver()


class Transaction(models.Model):
    payer = models.ForeignKey("Person", related_name="payer", on_delete=models.CASCADE)
    receiver = models.ForeignKey("Person", related_name="receiver", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)
    
    objects = TransactionManager()
    
    class Meta:
        verbose_name_plural = verbose_name_plural('Transactions')

    @property
    def is_transaction(self):
        return True

    def __str__(self):
        return str(self.amount) + " from " + self.payer.name + " to " + self.receiver.name\
               + " (room:" + self.payer.room.name + ")"
