from django.conf import settings
from django.test import override_settings, SimpleTestCase

from ..models import Payment


class TestPayment(SimpleTestCase):

    @override_settings(LANGUAGE_CODE='en', LANGUAGES=(('en', 'English'),))
    def test_str__en(self):
        payment = Payment(id=1, value=500.60)

        self.assertEqual('Id: 1, value: 500.6', str(payment))

    @override_settings(LANGUAGE_CODE='pt-BR', LANGUAGES=(('pt-br', 'Portuguese'),))
    def test_str__pt_br(self):
        payment = Payment(id=1, value=500.60)

        self.assertEqual('Id: 1, valor: 500.6', str(payment))
