from django.db import models
from django.utils.translation import ugettext_lazy as _


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    current_balance = models.FloatField()
    previous_balance = models.FloatField(null=True)

    class Meta:
        db_table = 'branch'
        verbose_name = _('Branch')
        verbose_name_plural = _('Branches')

    def __str__(self):
        return self.name
