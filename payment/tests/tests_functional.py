from freezegun import freeze_time
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Payment


class TestPaymentAPI(APITestCase):

    def setUp(self):
        self.path = '/v1/payments/'

    def _create_fixtures(self):
        mommy.make('Branch', id=1, name='Branch1')
        mommy.make('Branch', id=2, name='Branch2')

    def _create_payment_fixtures(self):
        mommy.make('Branch', previous_balance=0, current_balance=1000, _quantity=2)
        mommy.make('Payment', branch_id=1, is_paid=True, _quantity=3)
        mommy.make('Payment', branch_id=1, is_paid=False, expiration_date='2012-01-01', value=330.20, _quantity=2)
        mommy.make('Payment', id=10, branch_id=1, is_paid=False, expiration_date='2012-01-01', value=1100)

    def test_post__success(self):
        self._create_fixtures()

        expected_value = 50.3
        expected_expiration_date = '2019-05-01'
        expected_branch = 1
        data = dict(value=expected_value, expiration_date=expected_expiration_date, branch=expected_branch)

        response = self.client.post(path=self.path, data=data, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_200_OK, obtained_status)

        obtained_data = response.data
        self.assertEqual('Payment recorded successfully!', obtained_data['detail'])

        payment_obtained = obtained_data['data']
        self.assertTrue(payment_obtained['id'] > 0)
        self.assertEqual(expected_value, float(payment_obtained['value']))
        self.assertEqual(expected_expiration_date, payment_obtained['expiration_date'])
        self.assertEqual(expected_branch, payment_obtained['branch']['id'])

    def test_post__requirement_fail(self):
        expected_data = dict.fromkeys(['value', 'expiration_date', 'branch'], 'Required field')
        response = self.client.post(path=self.path, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, obtained_status)

        detail = response.data
        self.assertDictEqual(detail, expected_data)

    def test_post__branch_does_not_exists(self):
        branch_id = 99
        data = dict(value=50, expiration_date="2017-01-01", branch=branch_id)

        response = self.client.post(path=self.path, data=data, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, obtained_status)
        obtained = response.data

        self.assertEqual('Not found', obtained['branch'])

    def test_patch__payment_does_not_exists(self):
        payment_id = 99

        path = f'{self.path}{payment_id}/'
        response = self.client.patch(path=path, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_404_NOT_FOUND, obtained_status)

        obtained_data = response.data
        self.assertEqual('Payment not found', obtained_data['detail'])

    def test_patch__payment_is_already_paid(self):
        self._create_payment_fixtures()
        expected_message = 'This payment is already paid'

        path = f'{self.path}1/'
        response = self.client.patch(path=path, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, obtained_status)

        data = response.data
        self.assertEqual(data['detail'], expected_message)

    @freeze_time('2012-01-02')
    def test_patch__payment_is_due(self):
        self._create_payment_fixtures()
        expected_message = 'This payment is due'

        path = f'{self.path}4/'
        response = self.client.patch(path=path, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, obtained_status)

        data = response.data
        self.assertEqual(data['detail'], expected_message)

    @freeze_time('2012-01-01')
    def test_patch__value_is_higher_than_payment_amount(self):
        self._create_payment_fixtures()
        expected_message = 'Value to pay is higher than payment amount'

        path = f'{self.path}4/'
        response = self.client.patch(path=path, data={'value': 400}, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, obtained_status)

        data = response.data
        self.assertEqual(data['detail'], expected_message)

    @freeze_time('2012-01-01')
    def test_patch__branch_has_no_balance(self):
        self._create_payment_fixtures()
        expected_message = 'Branch has no balance'

        path = f'{self.path}10/'
        response = self.client.patch(path=path, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, obtained_status)

        data = response.data
        self.assertEqual(data['detail'], expected_message)

    @freeze_time('2012-01-01')
    def test_patch__specific_value__success(self):
        self._create_payment_fixtures()
        expected_message = 'Payment changed successfully!'
        payment_id = 4

        path = f'{self.path}{payment_id}/'
        response = self.client.patch(path=path, data={'value': 300}, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_200_OK, obtained_status)

        data = response.data
        self.assertEqual(data['detail'], expected_message)

        # Check results
        result = data['data']
        self.assertEqual(30.2, float(result['value']))

        # TODO: Check other fields changes
