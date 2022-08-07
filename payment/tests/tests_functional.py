from freezegun import freeze_time
from model_bakery import baker
from rest_framework import status

from commons.test import CustomAPITestCase


class TestPaymentAPI(CustomAPITestCase):
    def setUp(self):
        self.path = "/v1/payments/"

    def _create_fixtures(self):
        baker.make("Branch", id=1, name="Branch1")
        baker.make("Branch", id=2, name="Branch2")

    def _create_payment_fixtures(self):
        baker.make("Branch", id=1, previous_balance=0, current_balance=1000, _quantity=2)
        # Payment id 1-3
        baker.make("Payment", branch_id=1, is_paid=True, _quantity=3)
        # Payment id 4-5
        baker.make(
            "Payment",
            branch_id=1,
            is_paid=False,
            expiration_date="2012-01-01",
            value="330.20",
            _quantity=2,
        )
        # Payment id 10
        baker.make(
            "Payment",
            id=10,
            branch_id=1,
            is_paid=False,
            expiration_date="2012-01-01",
            value="1100.00",
        )

    def test_post__success(self):
        self._create_fixtures()

        expected_value = "50.30"
        expected_expiration_date = "2019-05-01"
        expected_branch = 1
        data = dict(
            value=expected_value,
            expiration_date=expected_expiration_date,
            branch=expected_branch,
        )

        response = self.send_post(path=self.path, data=data)

        self.assertResponse(response, status.HTTP_200_OK, "Payment recorded successfully!")

        obtained_data = response.data

        payment_obtained = obtained_data["data"]
        self.assertTrue(payment_obtained["id"] > 0)
        self.assertEqual(expected_value, payment_obtained["value"])
        self.assertEqual(expected_expiration_date, payment_obtained["expiration_date"])
        self.assertEqual(expected_branch, payment_obtained["branch"]["id"])

    def test_post__requirement_fail(self):
        expected_data = dict.fromkeys(["value", "expiration_date", "branch"], "Required field")
        response = self.send_post(path=self.path)

        self.assertResponse(response, status.HTTP_406_NOT_ACCEPTABLE)

        detail = response.data
        self.assertDictEqual(detail, expected_data)

    def test_post__branch_does_not_exists(self):
        branch_id = 99
        data = dict(value=50, expiration_date="2017-01-01", branch=branch_id)

        response = self.send_post(path=self.path, data=data)

        self.assertResponse(response, status.HTTP_406_NOT_ACCEPTABLE)
        obtained = response.data

        self.assertEqual("Not found", obtained["branch"])

    def test_patch__payment_does_not_exists(self):
        payment_id = 99

        path = f"{self.path}{payment_id}/"
        response = self.client.patch(path=path, HTTP_ACCEPT_LANGUAGE="en")

        self.assertResponse(response, status.HTTP_404_NOT_FOUND, "Payment not found")

    def test_patch__payment_is_already_paid(self):
        self._create_payment_fixtures()

        path = f"{self.path}1/"
        response = self.client.patch(path=path, HTTP_ACCEPT_LANGUAGE="en")

        self.assertResponse(response, status.HTTP_406_NOT_ACCEPTABLE, "This payment is already paid")

    @freeze_time("2012-01-02")
    def test_patch__payment_is_due(self):
        self._create_payment_fixtures()

        path = f"{self.path}4/"
        response = self.client.patch(path=path, HTTP_ACCEPT_LANGUAGE="en")

        self.assertResponse(response, status.HTTP_406_NOT_ACCEPTABLE, "This payment is due")

    @freeze_time("2012-01-01")
    def test_patch__value_is_higher_than_payment_amount(self):
        self._create_payment_fixtures()

        path = f"{self.path}4/"
        response = self.client.patch(path=path, data={"value": "400.00"}, HTTP_ACCEPT_LANGUAGE="en")

        self.assertResponse(
            response,
            status.HTTP_406_NOT_ACCEPTABLE,
            "Value to pay is higher than payment amount",
        )

    @freeze_time("2012-01-01")
    def test_patch__branch_has_no_balance(self):
        self._create_payment_fixtures()

        path = f"{self.path}10/"
        response = self.client.patch(path=path, HTTP_ACCEPT_LANGUAGE="en")

        self.assertResponse(response, status.HTTP_406_NOT_ACCEPTABLE, "Branch has no balance")

    @freeze_time("2012-01-01")
    def test_patch__specific_value__success(self):
        self._create_payment_fixtures()
        payment_id = 4

        path = f"{self.path}{payment_id}/"
        response = self.client.patch(path=path, data={"value": "300.00"}, HTTP_ACCEPT_LANGUAGE="en")

        self.assertResponse(response, status.HTTP_200_OK, "Payment changed successfully!")
        data = response.data

        # Check results
        result = data["data"]
        self.assertEqual("30.20", result["value"])
        self.assertIsNone(result["date_payment"])
        self.assertFalse(result["is_paid"])

        self.assertEqual("700.00", result["branch"]["current_balance"])
        self.assertEqual("1000.00", result["branch"]["previous_balance"])

    @freeze_time("2012-01-01")
    def test_patch__full_value__success(self):
        self._create_payment_fixtures()
        payment_id = 4

        path = f"{self.path}{payment_id}/"
        response = self.client.patch(path=path, data={"value": "330.20"}, HTTP_ACCEPT_LANGUAGE="en")

        self.assertResponse(response, status.HTTP_200_OK, "Payment changed successfully!")

        data = response.data

        # Check results
        result = data["data"]
        self.assertEqual("0.00", result["value"])
        self.assertEqual("2012-01-01", result["date_payment"])
        self.assertTrue(result["is_paid"])

        self.assertEqual("669.80", result["branch"]["current_balance"])
        self.assertEqual("1000.00", result["branch"]["previous_balance"])

    @freeze_time("2012-01-01")
    def test_patch__value_omitted__success(self):
        self._create_payment_fixtures()
        payment_id = 4

        path = f"{self.path}{payment_id}/"
        response = self.client.patch(path=path, HTTP_ACCEPT_LANGUAGE="en")

        self.assertResponse(response, status.HTTP_200_OK, "Payment changed successfully!")

        data = response.data

        # Check results
        result = data["data"]
        self.assertEqual("0.00", result["value"])
        self.assertEqual("2012-01-01", result["date_payment"])
        self.assertTrue(result["is_paid"])

        self.assertEqual("669.80", result["branch"]["current_balance"])
        self.assertEqual("1000.00", result["branch"]["previous_balance"])
