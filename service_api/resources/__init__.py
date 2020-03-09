from http import HTTPStatus
from typing import Dict, Union, Any, List

import aiohttp
from sanic.exceptions import ServerError
from sanic.views import HTTPMethodView


class ClientResponse:
    """Wrapper for response object.

    Args:
        status: response http status code.
        raw_content: content of response.
        json_data: response json data.
        headers: response http headers.

    """

    __slots__ = ("status", "raw_content", "json_data", "headers")

    def __init__(self, status: int, raw_content=None, json_data=None, headers=None):
        self.json_data = json_data
        self.status = status
        self.headers = headers
        self.raw_content = raw_content

    def get_content(self) -> Union[List[Dict], Dict[str, Any], str]:
        """Represents response data: json_data if provided else raw_content.

        Returns:
            Response data.

        """
        return self.json_data if self.json_data is not None else self.raw_content


class BaseView(HTTPMethodView):
    """Base class for application views.

    """

    REQUEST_TIMEOUT = 0

    async def __make_http_request(self, method: str, url: str, headers: Dict, data: Dict = None) -> ClientResponse:
        """Performs http requests.

        Args:
            method: type of request method.
            url: source address.
            headers: http request headers.
            data: request data.

        Returns:
             Response object.

        """
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

    async def make_get_request(self, url: str, headers: Dict = None) -> Union[List[Dict], Dict[str, Any], str]:
        """Performs http get request.

        Args:
            url: source address.
            headers: http request headers.

        Returns:
            Response data.

        Raises:
            ServerError: If response status not equal to 200.

        """
        response = await self.__make_http_request("GET", url, headers)
        if response.status != HTTPStatus.OK:
            error_message = f"Request failed: url={url}, status={response.status}, message={response.raw_content}"
            raise ServerError(error_message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            return response.get_content()
