from model_bakery import baker
from rest_framework import status

from commons.test import CustomAPITestCase
from ..models import Branch


class TestBranchAPI(CustomAPITestCase):

    def setUp(self):
        self.path = '/v1/branches/'

    def _create_branch_fixtures(self):
        baker.make('Branch', id=1, name='Test123')
        baker.make('Branch', _quantity=9)

    def _create_payment_fixtures(self):
        baker.make('Branch', _quantity=2)
        baker.make('Payment', branch_id=1, is_paid=True, _quantity=3)
        baker.make('Payment', branch_id=1, is_paid=False, _quantity=2)

    def test_post__success(self):
        expected_name = 'Branch A'
        expected_balance = 800.8
        data = dict(name=expected_name, current_balance=expected_balance)

        response = self.send_post(path=self.path, data=data)

        self.assertResponse(response, status.HTTP_200_OK, 'Branch recorded successfully!')

        branch_obtained = response.data['data']
        self.assertTrue(branch_obtained['id'] > 0)
        self.assertEqual(expected_name, branch_obtained['name'])
        self.assertEqual(expected_balance, float(branch_obtained['current_balance']))

    def test_post__requirement_fail(self):
        expected_detail = dict.fromkeys(['name', 'current_balance'], 'Required field')
        response = self.send_post(path=self.path)

        self.assertResponse(response, status.HTTP_406_NOT_ACCEPTABLE)

        detail = response.data
        self.assertDictEqual(detail, expected_detail)

    def test_put__branch_does_not_exists(self):
        self._create_branch_fixtures()

        branch_id = 99
        data = dict(name='AAA', current_balance=888)

        url = f'{self.path}{branch_id}/'
        response = self.client.put(path=url, data=data, HTTP_ACCEPT_LANGUAGE='en')

        self.assertResponse(response, status.HTTP_404_NOT_FOUND, 'Branch not found')

    def test_put__success(self):
        self._create_branch_fixtures()

        branch_id = 1

        expected_name = 'AAA'
        expected_balance = 888
        data = dict(name=expected_name, current_balance=expected_balance)

        url = f'{self.path}{branch_id}/'
        response = self.client.put(path=url, data=data, HTTP_ACCEPT_LANGUAGE='en')

        self.assertResponse(response, status.HTTP_200_OK, 'Branch updated successfully!')

        branch_obtained = response.data['data']
        self.assertEqual(branch_id, branch_obtained['id'])
        self.assertEqual(expected_name, branch_obtained['name'])
        self.assertEqual(expected_balance, float(branch_obtained['current_balance']))

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

        self.assertResponse(response, status.HTTP_200_OK)

        obtained = response.data
        self.assertTrue(obtained)
        self.assertEqual('Test123', obtained['name'])

    def test_get_by_id__no_data_found(self):
        self._create_branch_fixtures()
        branch_id = 99

        url = f'{self.path}{branch_id}/'
        response = self.client.get(url)

        self.assertResponse(response, status.HTTP_404_NOT_FOUND, 'Branch not found')

    def test_delete__not_found(self):
        self._create_branch_fixtures()
        branch_id = 99

        url = f'{self.path}{branch_id}/'
        response = self.client.delete(url, HTTP_ACCEPT_LANGUAGE='en')

        self.assertResponse(response, status.HTTP_404_NOT_FOUND, 'Branch not found')

    def test_delete__success(self):
        self._create_branch_fixtures()
        branch_id = 1

        url = f'{self.path}{branch_id}/'
        response = self.client.delete(url, HTTP_ACCEPT_LANGUAGE='en')

        self.assertResponse(response, status.HTTP_200_OK, 'Branch deleted successfully!')

        self.assertFalse(Branch.objects.filter(id=branch_id).exists())

    def test_get_payments__success(self):
        self._create_payment_fixtures()

        branch_id = 1
        response = self.client.get(path=f"{self.path}{branch_id}{'/payments/'}")

        self.assertResponse(response, status.HTTP_200_OK)

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

        self.assertResponse(response, status.HTTP_404_NOT_FOUND, 'Branch not found')

    def test_get_payments__is_paid(self):
        self._create_payment_fixtures()

        branch_id = 1
        is_paid = 'true'
        response = self.client.get(path=f"{self.path}{branch_id}{'/payments/'}", data={'is_paid': is_paid})

        self.assertResponse(response, status.HTTP_200_OK)

        total_obtained = len(response.data)

        self.assertEqual(3, total_obtained)

    def test_get_payment__is_not_paid(self):
        self._create_payment_fixtures()

        branch_id = 1
        is_paid = False
        response = self.client.get(path=f"{self.path}{branch_id}{'/payments/'}", data={'is_paid': is_paid})

        self.assertResponse(response, status.HTTP_200_OK)

        total_obtained = len(response.data)

        self.assertEqual(2, total_obtained)
