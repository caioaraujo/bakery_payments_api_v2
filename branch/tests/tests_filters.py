from django.test import SimpleTestCase

from ..views import BranchPaymentsView
from ..filters import PaymentFilterBackend


class TestPaymentFilterBackend(SimpleTestCase):
    def test_fields(self):
        payment_filter = PaymentFilterBackend()

        schema_fields = payment_filter.get_schema_fields(BranchPaymentsView)

        self.assertEqual(1, len(schema_fields))

        is_paid_filter = schema_fields[0]
        self.assertFalse(is_paid_filter.required)
        self.assertEqual(is_paid_filter.location, "query")
