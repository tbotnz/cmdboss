import logging
import importlib

from typing import List, Union, Optional

from fastapi import APIRouter, Request, Query

from fastapi.encoders import jsonable_encoder

from backend.conf.confload import config

from backend.cmdboss_db.cmdboss_db import CMDBOSS_db

from backend.models.system import (
    ResponseBasic,
    CMDBOSSQuery
)

from routers.route_utils import (
    HttpErrorHandler
)

from backend.util.file_mgr import func_retrieve_files

log = logging.getLogger(__name__)


payload = {}
payload["route_type"] = "model"

router = APIRouter()

routes = func_retrieve_files(payload)

if len(routes["result"]) >= 1:
    for model_name in routes["result"]:
        try:

            # load model
            model_path_raw = config.model_dir
            model_path = model_path_raw.replace('/', '.') + model_name
            module = importlib.import_module(model_path)
            model_data = getattr(module, model_name)

            # create routes
            @router.post(
                        f"/table/{model_name}",
                        response_model=ResponseBasic,
                        status_code=201,
                        summary=f"Create one or many {model_name} objects"
                        )
            @HttpErrorHandler()
            async def create(
                            model_payload: Union[model_data, List[model_data]],
                            request: Request
                            ):
                cmdboss = CMDBOSS_db()
                result = cmdboss.insert(model_instance_data=model_payload, path=f"{request.url}")
                return jsonable_encoder(result)

            # retrieve routes
            @router.get(
                        f"/table/{model_name}",
                        response_model=ResponseBasic,
                        status_code=200,
                        summary=f"Retrieve many {model_name} objects"
                        )
            @router.get(
                        f"/table/{model_name}/"+"{object_id}",
                        response_model=ResponseBasic,
                        status_code=200,
                        summary=f"Retrieve a single {model_name} object"
                        )
            @HttpErrorHandler()
            async def retrieve(request: Request, query: Optional[CMDBOSSQuery] = {}, object_id: Optional[str] = None):
                q = {}
                if query:
                    q = query.dict()
                cmdboss = CMDBOSS_db()
                result = cmdboss.retrieve(query_obj=q, object_id=object_id, path=f"{request.url}")
                return jsonable_encoder(result)

            # update routes
            @router.patch(
                        f"/table/{model_name}/",
                        response_model=ResponseBasic,
                        status_code=200,
                        summary=f"Update many {model_name} objects"
                        )
            @router.patch(
                        f"/table/{model_name}/"+"{object_id}",
                        response_model=ResponseBasic,
                        status_code=200,
                        summary=f"Update a single {model_name} object"
                        )
            @HttpErrorHandler()
            async def update(
                          model_payload: model_data,
                          request: Request,
                          object_id: Optional[str] = None
                          ):
                cmdboss = CMDBOSS_db()
                result = cmdboss.update(model_instance_data=model_payload, object_id=object_id, path=f"{request.url}")
                return jsonable_encoder(result)

            # delete routes
            @router.delete(
                        f"/table/{model_name}",
                        response_model=ResponseBasic,
                        status_code=200,
                        summary=f"Delete many {model_name} objects"
                        )
            @router.delete(
                        f"/table/{model_name}/"+"{object_id}",
                        response_model=ResponseBasic,
                        status_code=200,
                        summary=f"Delete a single {model_name} object"
                        )
            @HttpErrorHandler()
            async def delete(request: Request, query: Optional[CMDBOSSQuery] = {} , object_id: Optional[str] = None):
                q = {}
                if query:
                    q = query.dict()
                cmdboss = CMDBOSS_db()
                result = cmdboss.delete(query=q, object_id=object_id, path=f"{request.url}")
                return jsonable_encoder(result)

        except Exception as e:
            log.error(f"user model error: error {e} loading model {model_name} - please check the class name matches the model name")