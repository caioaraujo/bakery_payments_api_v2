from django.db import models
from django.utils.translation import ugettext


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.FloatField()
    expiration_date = models.DateField()
    date_payment = models.DateField(null=True)
    branch = models.ForeignKey('branch.Branch', on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = 'payment'
        verbose_name = ugettext('Payment')
        verbose_name_plural = ugettext('Payments')

    def __str__(self):
        return f"Id: {self.id} {ugettext('value')}: {self.value}"
