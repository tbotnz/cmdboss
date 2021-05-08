import logging
import socket

from fastapi.openapi.utils import get_openapi

from backend.conf.confload import config
from backend.util.exceptions import (
    CMDBOSSCallbackHTTPException
)

log = logging.getLogger(__name__)


def custom_openapi(app):
    openapi_schema = get_openapi(
        title="cmdboss",
        version="1.0.0",
        description="",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://raw.githubusercontent.com/tbotnz/cmdboss/main/cmdboss.PNG"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
