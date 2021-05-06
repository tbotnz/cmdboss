
import importlib

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse

from backend.conf.confload import config
from backend.security.get_api_key import get_api_key
from backend.util.exceptions import (
    CMDBOSSHTTPException
)
from backend.util.oapi import custom_openapi

from routers import (
    system,
    usr_models
)

config.setup_logging(max_debug=True)

app = FastAPI()

app.include_router(system.router, dependencies=[Depends(get_api_key)])

@app.exception_handler(CMDBOSSHTTPException)
async def unicorn_exception_handler(
                                    request: Request,
                                    exc: CMDBOSSHTTPException
                                    ):
    return JSONResponse(
                        status_code=500,
                        content={
                            "status": f"{exc.status}",
                            "result": exc.result
                            },
                        )

custom_openapi(app)

@app.post("/refresh", include_in_schema=False, status_code=201)
async def refresh():
    importlib.reload(usr_models)
    app.include_router(usr_models.router, dependencies=[Depends(get_api_key)])
    custom_openapi(app)
    return True
