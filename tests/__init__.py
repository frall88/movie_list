from asynctest import TestCase
from service_api.app import app


class BaseTestCase(TestCase):
    @property
    def app(self):
        return app
