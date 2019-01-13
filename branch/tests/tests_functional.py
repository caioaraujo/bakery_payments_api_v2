from rest_framework import status
from rest_framework.test import APITestCase


class TestBranchAPI(APITestCase):

    def test_post__success(self):
        data = dict(name='Branch A', current_balance=800.8)

        response = self.client.post(path='/branches/', data=data)

        obtained_status = response.status_code
        self.assertEqual(status.HTTP_200_OK, obtained_status)
