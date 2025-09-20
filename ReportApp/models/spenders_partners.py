from django.db import models

from ReportApp.models._base import verbose_name_plural


class Spenders(models.Model):
    weight = models.IntegerField(default=1)
    spender_person = models.ForeignKey("Person", on_delete=models.CASCADE, default=None)
    spender_spend = models.ForeignKey("Spend", on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name_plural = verbose_name_plural('spender (Person m2m Spend)')

    def __str__(self):
        return "spender " + str(self.spender_person.id) + " <--> " + str(self.spender_spend.id) + " spend"


class Partners(models.Model):
    weight = models.IntegerField(default=1)
    partner_person = models.ForeignKey("Person", on_delete=models.CASCADE, default=None)
    partner_spend = models.ForeignKey("Spend", on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name_plural = verbose_name_plural('partner (Person m2m Spend)')

    def __str__(self):
        return "partner " + str(self.partner_person.id) + " <--> " + str(self.partner_spend.id) + " spend"
