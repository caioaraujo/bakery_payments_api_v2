from branch.models import Branch
from commons.decorators import validate_requirements, validate_existance
from .models import Payment


class PaymentService:

    @validate_requirements('value', 'expiration_date', 'branch')
    @validate_existance((Branch, 'branch'))
    def insert(self, params):
        value = params['value']
        expiration_date = params['expiration_date']
        branch = params['branch']

        payment = Payment(value=value, expiration_date=expiration_date, branch_id=branch)

        payment.save()

        return payment

    @validate_existance((Payment, 'id'), is_critical=True)
    def change_paid_status(self, params):
        # TODO
        pass
