from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Branch


class TestBranchAPI(APITestCase):

    def setUp(self):
        self.path = '/v1/branches/'

    def _create_branch_fixtures(self):
        mommy.make('Branch', id=1, name='Test123')
        mommy.make('Branch', _quantity=9)

    def _create_payment_fixtures(self):
        mommy.make('Branch', _quantity=2)
        mommy.make('Payment', branch_id=1, is_paid=True, _quantity=3)
        mommy.make('Payment', branch_id=1, is_paid=False, _quantity=2)

    def test_post__success(self):
        expected_name = 'Branch A'
        expected_balance = 800.8
        data = dict(name=expected_name, current_balance=expected_balance)

        response = self.client.post(path=self.path, data=data, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_200_OK, obtained_status)

        obtained_data = response.data
        self.assertEqual('Branch recorded successfully!', obtained_data['detail'])

        branch_obtained = obtained_data['data']
        self.assertTrue(branch_obtained['id'] > 0)
        self.assertEqual(expected_name, branch_obtained['name'])
        self.assertEqual(expected_balance, branch_obtained['current_balance'])

    def test_post__requirement_fail(self):
        expected_message = 'Required field'
        response = self.client.post(path=self.path)

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, obtained_status)

        detail = response.data
        self.assertEqual(detail['name'], expected_message)
        self.assertEqual(detail['current_balance'], expected_message)

    def test_put__does_not_exists(self):
        self._create_branch_fixtures()

        branch_id = 99
        data = dict(name='AAA', current_balance=888)

        url = f'{self.path}{branch_id}/'
        response = self.client.put(path=url, data=data, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_404_NOT_FOUND, obtained_status)

        obtained_data = response.data
        self.assertEqual('Branch not found', obtained_data['detail'])

    def test_put__success(self):
        self._create_branch_fixtures()

        branch_id = 1

        expected_name = 'AAA'
        expected_balance = 888
        data = dict(name=expected_name, current_balance=expected_balance)

        url = f'{self.path}{branch_id}/'
        response = self.client.put(path=url, data=data, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_200_OK, obtained_status)

        obtained_data = response.data
        self.assertEqual('Branch updated successfully!', obtained_data['detail'])

        branch_obtained = obtained_data['data']
        self.assertEqual(branch_id, branch_obtained['id'])
        self.assertEqual(expected_name, branch_obtained['name'])
        self.assertEqual(expected_balance, branch_obtained['current_balance'])

    def test_get__success(self):
        self._create_branch_fixtures()

        response = self.client.get(self.path)

        obtained_data = response.data

        self.assertTrue(len(obtained_data))
        self.assertEqual(10, len(obtained_data))

    def test_get__no_data_found(self):
        response = self.client.get(self.path)

        obtained_data = response.data
        self.assertFalse(len(obtained_data))

    def test_get_by_id__success(self):
        self._create_branch_fixtures()

        branch_id = 1

        url = f'{self.path}{branch_id}/'
        response = self.client.get(url)

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_200_OK, obtained_status)

        obtained = response.data
        self.assertTrue(obtained)
        self.assertEqual('Test123', obtained['name'])

    def test_get_by_id__no_data_found(self):
        self._create_branch_fixtures()
        branch_id = 99

        url = f'{self.path}{branch_id}/'
        response = self.client.get(url)

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_404_NOT_FOUND, obtained_status)

        detail = response.data['detail']

        self.assertEqual('Branch not found', detail)

    def test_delete__not_found(self):
        self._create_branch_fixtures()
        branch_id = 99

        url = f'{self.path}{branch_id}/'
        response = self.client.delete(url, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_404_NOT_FOUND, obtained_status)

        detail = response.data['detail']

        self.assertEqual('Branch not found', detail)

    def test_delete__success(self):
        self._create_branch_fixtures()
        branch_id = 1

        url = f'{self.path}{branch_id}/'
        response = self.client.delete(url, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_200_OK, obtained_status)

        detail = response.data['detail']

        self.assertEqual('Branch deleted successfully!', detail)

        self.assertFalse(Branch.objects.filter(id=branch_id).exists())

    def test_get_payments__success(self):
        self._create_payment_fixtures()

        branch_id = 1
        response = self.client.get(path=f"{self.path}{branch_id}{'/payments/'}")

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_200_OK, obtained_status)

        total_obtained = len(response.data)

        self.assertEqual(5, total_obtained)

    def test_get_payments__no_data_found(self):
        self._create_payment_fixtures()

        branch_id = 2
        response = self.client.get(path=f"{self.path}{branch_id}{'/payments/'}")

        obtained_data = response.data
        self.assertFalse(len(obtained_data))

    def test_get_payments__branch_does_not_exists(self):
        self._create_payment_fixtures()

        branch_id = 99
        response = self.client.get(path=f"{self.path}{branch_id}{'/payments/'}")

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_404_NOT_FOUND, obtained_status)

        obtained_detail = response.data['detail']

        self.assertEqual('Branch not found', obtained_detail)

    def test_get_payments__is_paid(self):
        self._create_payment_fixtures()

        branch_id = 1
        is_paid = 'true'
        response = self.client.get(path=f"{self.path}{branch_id}{'/payments/'}", data={'is_paid': is_paid})

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_200_OK, obtained_status)

        total_obtained = len(response.data)

        self.assertEqual(3, total_obtained)

    def test_get_payment__is_not_paid(self):
        self._create_payment_fixtures()

        branch_id = 1
        is_paid = False
        response = self.client.get(path=f"{self.path}{branch_id}{'/payments/'}", data={'is_paid': is_paid})

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_200_OK, obtained_status)

        total_obtained = len(response.data)

        self.assertEqual(2, total_obtained)
