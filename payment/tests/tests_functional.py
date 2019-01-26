from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase


class TestPaymentAPI(APITestCase):

    def setUp(self):
        self.path = '/payments/'
        self._create_fixtures()

    def _create_fixtures(self):
        mommy.make('Branch', id=1, name='Branch1')
        mommy.make('Branch', id=2, name='Branch2')

    def test_post__success(self):
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
        self.assertEqual(expected_value, payment_obtained['value'])
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
