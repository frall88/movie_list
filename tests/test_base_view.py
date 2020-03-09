from http import HTTPStatus

from asynctest import patch, CoroutineMock
from sanic.exceptions import ServerError

from service_api.resources import BaseView, ClientResponse
from tests import BaseTestCase


class TestBaseView(BaseTestCase):
    async def test_make_get_request_ok(self):
        ok_content = "Python"
        with patch(
            "service_api.resources.BaseView._BaseView__make_http_request",
            CoroutineMock(return_value=ClientResponse(HTTPStatus.OK, ok_content)),
        ):
            resp = await BaseView().make_get_request("url_string")
            self.assertEqual(resp, ok_content)

    async def test_make_get_request_error(self):
        with patch(
            "service_api.resources.BaseView._BaseView__make_http_request",
            CoroutineMock(return_value=ClientResponse(HTTPStatus.BAD_REQUEST)),
        ):
            with self.assertRaises(ServerError):
                await BaseView().make_get_request("url_string")
