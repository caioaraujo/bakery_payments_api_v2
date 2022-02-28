from django.db import models
from django.utils.translation import gettext_lazy as _


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2)
    previous_balance = models.DecimalField(null=True, max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'branch'
        ordering = ['-id']
        verbose_name = _('Branch')
        verbose_name_plural = _('Branches')

    def __str__(self):
        return self.name
