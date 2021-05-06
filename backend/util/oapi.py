import logging
import httpx
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


def reload_routes():
    log.info("reload_routes: model change occuring")
    headers = {
        config.api_key_name: config.api_key,
        "Content-Type": "application/json"
    }
    hostname = socket.gethostname()
    r = httpx.post(
                f"{config.cmdboss_http_https}://{hostname}:{config.listen_port}/refresh",
                timeout=30,
                headers=headers,
                verify=False,
                data={}
                )
    print(r.status_code)
    log.info("reload_routes: model change complete")