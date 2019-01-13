from django.db import models
from django.utils.translation import ugettext_lazy as _


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.FloatField()
    expiration_date = models.DateField()
    date_payment = models.DateField(null=True)
    branch = models.ForeignKey('branch.Branch', on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = 'payment'
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        value_txt = _('value')
        return f"Id: {self.id}, {value_txt}: {self.value}"
