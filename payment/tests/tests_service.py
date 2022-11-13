from unittest import mock
from unittest import TestCase

from ..services import PaymentService


class PaymentServiceTest(TestCase):

    @mock.patch("payment.models.Payment")
    def test_insert__success(self, payment_mock):
        service = PaymentService()
        value = "32.00"
        expiration_date = "2025-01-01"
        branch = 1
        params = {"value": value, "expiration_date": expiration_date, "branch": branch}
        service.insert(params)

        payment_mock.assert_called_once_with(value=value, expiration_date=expiration_date, branch_id=branch)
