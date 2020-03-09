from sanic.app import Sanic

from service_api import api_v1
from service_api.config import runtime_config
from service_api.constants import DEFAULT_SERVICE_NAME
from service_api.exceptions import setup_exception_handler


app = Sanic(DEFAULT_SERVICE_NAME)
app.config.from_object(runtime_config())
api_v1.load_api(app)
setup_exception_handler(app)
