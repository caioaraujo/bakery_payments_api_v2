from django.core.exceptions import ImproperlyConfigured
from django.core.servers.basehttp import get_internal_wsgi_application
from django.test import SimpleTestCase, override_settings

from ..wsgi import application


class TestWsgi(SimpleTestCase):
    def test__success(self):

        app = get_internal_wsgi_application()

        self.assertIs(app, application)

    @override_settings(WSGI_APPLICATION="wsgi.noexist.app")
    def test__module_failure(self):
        expect_message = (
            "WSGI application 'wsgi.noexist.app' could not be loaded; Error importing"
        )
        with self.assertRaisesMessage(ImproperlyConfigured, expect_message):
            get_internal_wsgi_application()
