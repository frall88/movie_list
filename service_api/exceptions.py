import logging
from traceback import format_exc

from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.response import json

logger = logging.getLogger(__name__)


def setup_exception_handler(app: Sanic):
    app.exception(Exception)(default_exception_handler)


def default_exception_handler(request, exception):
    logger.error(format_exc())
    if issubclass(type(exception), ApplicationError):
        message = str(exception)
    else:
        message = repr(exception)
    return json(
        {"error_message": message},
        status=getattr(exception, "status_code", 500),
        headers=getattr(exception, "headers", {"Content-type": "application/json"}),
    )


class ApplicationError(SanicException):
    pass
