from rest_framework import status
from rest_framework.test import APITestCase


class TestBranchAPI(APITestCase):

    def test_post__success(self):
        expected_name = 'Branch A'
        expected_balance = 800.8
        data = dict(name=expected_name, current_balance=expected_balance)

        response = self.client.post(path='/branches/', data=data, HTTP_ACCEPT_LANGUAGE='en')

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
        response = self.client.post(path='/branches/')

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, obtained_status)

        detail = response.data
        self.assertEqual(detail['name'], expected_message)
        self.assertEqual(detail['current_balance'], expected_message)
