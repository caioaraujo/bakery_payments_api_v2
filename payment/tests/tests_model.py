from django.test import override_settings, TestCase
from model_bakery import baker
from rest_framework.exceptions import APIException

from ..models import Payment


class TestPayment(TestCase):

    def _create_payment_fixtures(self):
        baker.make('Branch')
        baker.make('Payment', id=1, branch_id=1, value=34.5)

    @override_settings(LANGUAGE_CODE='en', LANGUAGES=(('en', 'English'),))
    def test_str__en(self):
        payment = Payment(id=1, value=500.60)

        self.assertEqual('Id: 1, value: 500.6', str(payment))

    @override_settings(LANGUAGE_CODE='pt-BR', LANGUAGES=(('pt-br', 'Portuguese'),))
    def test_str__pt_br(self):
        payment = Payment(id=1, value=500.60)

        self.assertEqual('Id: 1, valor: 500.6', str(payment))

    @override_settings(LANGUAGE_CODE='en', LANGUAGES=(('en', 'English'),))
    def test_find_flat_values__payment_does_not_exists(self):
        payment_id = 99

        with self.assertRaisesMessage(APIException, 'Payment does not exists'):
            Payment.find_single_values(payment_id, 'value')

    def test_find_flat_values__single_value(self):
        self._create_payment_fixtures()

        payment_id = 1

        value = Payment.find_single_values(payment_id, 'value')
        self.assertEqual(34.5, value)

    def test_find_flat_values__many_values(self):
        self._create_payment_fixtures()

        payment_id = 1

        value, branch_id = Payment.find_single_values(payment_id, 'value', 'branch_id')
        self.assertEqual(34.5, value)
        self.assertEqual(1, branch_id)
