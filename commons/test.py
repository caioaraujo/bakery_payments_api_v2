from rest_framework.test import APITestCase


class CustomAPITestCase(APITestCase):

    def send_post(self, path, data=None, format=None, content_type=None, follow=False,
                  http_accept_language='en', **extra):

        extra['HTTP_ACCEPT_LANGUAGE'] = http_accept_language
        return self.client.post(path, data, format, content_type, follow, **extra)

    def assertResponse(self, response, status_code, detail=None):
        obtained_status = response.status_code
        self.assertEqual(status_code, obtained_status)

        if detail:
            obtained_data = response.data
            self.assertEqual(detail, obtained_data['detail'])
