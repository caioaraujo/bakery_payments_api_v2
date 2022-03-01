from django.db import models
from django.utils.translation import gettext_lazy as _, gettext
from rest_framework.exceptions import APIException


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    expiration_date = models.DateField()
    date_payment = models.DateField(null=True)
    branch = models.ForeignKey("branch.Branch", on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    @classmethod
    def find_single_values(cls, payment_id, *field_names):
        """
        Query specific value(s) from a single payment

        Args:
            payment_id: int
            *field_names: Payment model field names

        Returns: A single value or a tuple of many values

        """
        is_flat = len(field_names) == 1

        try:
            return cls.objects.values_list(*field_names, flat=is_flat).get(
                id=payment_id
            )
        except Payment.DoesNotExist:
            raise APIException(detail=gettext("Payment does not exists"))

    class Meta:
        db_table = "payment"
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        value_txt = _("value")
        return f"Id: {self.id}, {value_txt}: {self.value}"
