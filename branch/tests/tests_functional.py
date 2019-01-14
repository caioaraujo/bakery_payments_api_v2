from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Branch


class TestBranchAPI(APITestCase):

    def setUp(self):
        self.path = '/branches/'
        self._create_fixtures()

    def _create_fixtures(self):
        mommy.make('Branch', id=1, name='Test123')
        mommy.make('Branch', _quantity=9)

    def test_post__success(self):
        expected_name = 'Branch A'
        expected_balance = 800.8
        data = dict(name=expected_name, current_balance=expected_balance)

        response = self.client.post(path=self.path, data=data, HTTP_ACCEPT_LANGUAGE='en')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_200_OK, obtained_status)

        obtained_data = response.data
        self.assertEqual('Branch recorded successfully!', obtained_data['message'])

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

    def test_get__success(self):
        response = self.client.get(self.path)

        obtained_data = response.data

        self.assertTrue(len(obtained_data))
        self.assertEqual(10, len(obtained_data))

    def test_get__no_data_found(self):
        Branch.objects.all().delete()

        response = self.client.get(self.path)

        obtained_data = response.data
        self.assertFalse(len(obtained_data))

    def test_get_by_id__success(self):
        branch_id = 1

        url = f'{self.path}{branch_id}/'
        response = self.client.get(url)

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_200_OK, obtained_status)

        obtained = response.data
        self.assertTrue(obtained)
        self.assertEqual('Test123', obtained['name'])

    def test_get_by_id__no_data_found(self):
        branch_id = 99

        url = f'{self.path}{branch_id}/'
        response = self.client.get(url)

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_204_NO_CONTENT, obtained_status)

        obtained = response.data
        self.assertIsNone(obtained)
