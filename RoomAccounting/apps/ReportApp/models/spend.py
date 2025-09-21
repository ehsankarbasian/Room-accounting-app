from django.db import models
from django.db.models import Prefetch

from apps.ReportApp.models._base import verbose_name_plural, DefaultZeroDict

from apps.ReportApp.models import Spenders, Partners


class SpendQuerySet(models.QuerySet):
    
    def prefetch_with_spenders_and_partners(self):
        return self.prefetch_related(
                Prefetch(
                    "spenders_set",
                    queryset=Spenders.objects.select_related("spender_person"),
                    to_attr="prefetched_spenders"
                ),
                Prefetch(
                    "partners_set",
                    queryset=Partners.objects.select_related("partner_person"),
                    to_attr="prefetched_partners"
                )
            )


class SpendManager(models.Manager):
    
    def get_queryset(self):
        return SpendQuerySet(self.model, using=self._db)

    def prefetch_with_spenders_and_partners(self):
        return self.get_queryset().prefetch_with_spenders_and_partners()


class Spend(models.Model):
    amount = models.IntegerField(default=0)
    description = models.CharField(max_length=256, blank=True)
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    
    objects = SpendManager()

    class Meta:
        verbose_name_plural = verbose_name_plural('Spends')

    @property
    def related_persons(self):
        not_related_persons = self.room.person_set.all()
        for spender in self.spenders_set.all():
            if spender.spender_person in not_related_persons:
                not_related_persons = not_related_persons.exclude(id=spender.spender_person.id)

        related_persons = self.room.person_set.all()
        for person in not_related_persons:
            related_persons = related_persons.exclude(id=person.id)
            
        return related_persons

    @property
    def partner_dict(self):
        result = DefaultZeroDict()

        for partner in self.prefetched_partners:
            result[partner.partner_person.id] = partner.weight

        return result

    @property
    def spender_dict(self):
        result = DefaultZeroDict()

        for spender in self.prefetched_spenders:
            result[spender.spender_person.id] = spender.weight

        return result

    @property
    def is_transaction(self):
        return False

    def __str__(self):
        return str(self.amount) + " for " + self.description + " (room:" + self.room.name + ")"
