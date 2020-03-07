from http import HTTPStatus
from typing import Dict, Union, Any

import aiohttp
from sanic.exceptions import ServerError
from sanic.views import HTTPMethodView


class ClientResponse:
    __slots__ = ("status", "raw_content", "json_data", "headers")

    def __init__(self, status: int, raw_content=None, json_data=None, headers=None):
        self.json_data = json_data
        self.status = status
        self.headers = headers
        self.raw_content = raw_content

    def get_content(self) -> Union[Dict[str, Any], str]:
        return self.json_data if self.json_data is not None else self.raw_content


class BaseView(HTTPMethodView):
    REQUEST_TIMEOUT = 0

    async def make_http_request(self, method: str, url: str, headers: Dict, data: Dict = None) -> ClientResponse:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method, url=url, data=data, headers=headers, timeout=self.REQUEST_TIMEOUT
            ) as response:
                try:
                    request_json = await response.json()
                except aiohttp.ContentTypeError:
                    return ClientResponse(
                        raw_content=response.content, status=response.status, headers=response.headers
                    )

                return ClientResponse(json_data=request_json, status=response.status, headers=response.headers)

    async def get_request(self, url: str, headers: Dict = None):
        response = await self.make_http_request("GET", url, headers)
        if response.status != HTTPStatus.OK:
            error_message = f"Request failed: url={url}, status={response.status}, message={response.raw_content}"
            raise ServerError(error_message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            return response.get_content()
