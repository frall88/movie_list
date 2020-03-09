from service_api.resources import ClientResponse
from tests import BaseTestCase


class TestClientResponse(BaseTestCase):
    def test_get_content_json_data(self):
        data = [{"key": "foo"}, {"key": "bar"}]
        cr = ClientResponse(200, json_data=data)
        actual_result = cr.get_content()
        self.assertListEqual(actual_result, data)

    def test_get_content_raw_data(self):
        data = "Some response text message."
        cr = ClientResponse(200, raw_content=data)
        actual_result = cr.get_content()
        self.assertEqual(actual_result, data)
