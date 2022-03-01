from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.exceptions import NotAcceptable

from branch.models import Branch
from commons.decorators import validate_requirements, validate_existance
from .models import Payment


class PaymentService:
    @validate_requirements("value", "expiration_date", "branch")
    @validate_existance((Branch, "branch"))
    def insert(self, params):
        value = params["value"]
        expiration_date = params["expiration_date"]
        branch = params["branch"]

        payment = Payment(value=value, expiration_date=expiration_date, branch_id=branch)

        payment.save()

        return payment

    @validate_existance((Payment, "id"), is_critical=True)
    @transaction.atomic
    def pay(self, params):
        payment_id = params["id"]

        fields_to_query = ("is_paid", "expiration_date", "value", "branch_id")
        is_paid, expiration_date, current_value, branch_id = Payment.find_single_values(payment_id, *fields_to_query)
        current_value = float(current_value)

        # Check if payment is already paid
        if is_paid:
            raise NotAcceptable(detail=_("This payment is already paid"))

        # Check expiration date
        current_date = timezone.now().date()
        if expiration_date < current_date:
            raise NotAcceptable(detail=_("This payment is due"))

        value_to_pay = params.get("value")
        date_payment = None
        is_paid = False

        if value_to_pay:

            # Check amount
            if value_to_pay > current_value:
                raise NotAcceptable(detail=_("Value to pay is higher than payment amount"))

            if value_to_pay == current_value:
                is_paid = True
                date_payment = current_date
            current_value = current_value - value_to_pay
        else:
            value_to_pay = current_value
            current_value = 0
            is_paid = True
            date_payment = current_date

        self._update_branch_balance(branch_id, value_to_pay)

        payment = Payment(
            id=payment_id,
            is_paid=is_paid,
            value=current_value,
            date_payment=date_payment,
        )
        payment.save(update_fields=["is_paid", "value", "date_payment"])

        return Payment.objects.get(id=payment_id)

    def _update_branch_balance(self, branch_id, amount_to_discount):
        current_branch_balance = Branch.objects.values_list("current_balance", flat=True).get(id=branch_id)
        current_branch_balance = float(current_branch_balance)

        if amount_to_discount > current_branch_balance:
            raise NotAcceptable(detail=_("Branch has no balance"))

        old_branch_balance = current_branch_balance
        current_branch_balance = current_branch_balance - amount_to_discount
        branch = Branch(
            id=branch_id,
            previous_balance=old_branch_balance,
            current_balance=current_branch_balance,
        )

        branch.save(update_fields=["previous_balance", "current_balance"])
