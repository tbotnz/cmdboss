import logging

from typing import Optional

from fastapi import APIRouter, Request, Query
from fastapi.encoders import jsonable_encoder

from backend.cmdboss_db.cmdboss_db import CMDBOSS_db

from backend.models.system import (
    SysModelIngest,
    ResponseBasic,
    Hook,
    CMDBOSSQuery
)

from routers.route_utils import HttpErrorHandler


log = logging.getLogger(__name__)

router = APIRouter()


@router.post("/models/{model_name}", response_model=ResponseBasic, status_code=201)
@HttpErrorHandler()
async def create_model(request: Request, model_payload: SysModelIngest, model_name: str):
    model_payload.name = model_name
    cmdboss = CMDBOSS_db()
    result = cmdboss.insert(model_instance_data=model_payload, path=f"{request.url}")
    # reload_routes()
    return jsonable_encoder(result)


# delete routes
@router.delete(
            f"/models/"+"{object_id}",
            response_model=ResponseBasic,
            status_code=200,
            summary=f"Delete a single model object"
            )
@HttpErrorHandler()
async def delete_model(request: Request, query: Optional[CMDBOSSQuery] = None,  object_id: Optional[str] = None):
    q = {}
    if query:
        q = query.dict()
    cmdboss = CMDBOSS_db()
    result = cmdboss.delete(query=q, object_id=object_id, path=f"{request.url}")
    return jsonable_encoder(result)


@router.get(
            f"/models",
            response_model=ResponseBasic,
            status_code=200,
            summary=f"Retrieve many model objects"
            )
@router.get(
            f"/models/"+"{object_id}",
            response_model=ResponseBasic,
            status_code=200,
            summary=f"Retrieve a single model object"
            )
@HttpErrorHandler()
async def retrieve_models(request: Request, query: Optional[CMDBOSSQuery] = None, object_id: Optional[str] = None):
    q = {}
    if query:
        q = query.dict()
    cmdboss = CMDBOSS_db()
    result = cmdboss.retrieve(query_obj=q, object_id=object_id, path=f"{request.url}")
    return jsonable_encoder(result)

@router.patch(
            f"/models/"+"{object_id}",
            response_model=ResponseBasic,
            status_code=200,
            summary=f"Update a single model object"
            )
@HttpErrorHandler()
async def update(
                model_payload: SysModelIngest,
                request: Request,
                object_id: Optional[str] = None
                ):
    cmdboss = CMDBOSS_db()
    result = cmdboss.update(model_instance_data=model_payload, object_id=object_id, path=f"{request.url}")
    return jsonable_encoder(result)


@router.post("/hooks", response_model=ResponseBasic, status_code=201)
@HttpErrorHandler()
async def create_hook(hook_payload: Hook, request: Request):
    cmdboss = CMDBOSS_db()
    result = cmdboss.insert(model_instance_data=hook_payload, path=f"{request.url}")
    return jsonable_encoder(result)

# delete routes
@router.delete(
            f"/hooks/"+"{object_id}",
            response_model=ResponseBasic,
            status_code=200,
            summary=f"Delete a single hook object"
            )
@HttpErrorHandler()
async def delete(request: Request, query: Optional[CMDBOSSQuery] = None,  object_id: Optional[str] = None):
    q = {}
    if query:
        q = query.dict()
    cmdboss = CMDBOSS_db()
    result = cmdboss.delete(query=q, object_id=object_id, path=f"{request.url}")
    return jsonable_encoder(result)

@router.get(
            f"/hooks",
            response_model=ResponseBasic,
            status_code=200,
            summary=f"Retrieve many hook objects"
            )
@router.get(
            f"/hooks/"+"{object_id}",
            response_model=ResponseBasic,
            status_code=200,
            summary=f"Retrieve a single hook object"
            )
@HttpErrorHandler()
async def retrieve_hooks(request: Request, query: Optional[CMDBOSSQuery] = None, object_id: Optional[str] = None):
    q = {}
    if query:
        q = query.dict()
    cmdboss = CMDBOSS_db()
    result = cmdboss.retrieve(query_obj=q, object_id=object_id, path=f"{request.url}")
    return jsonable_encoder(result)


@router.patch(
            f"/hooks/"+"{object_id}",
            response_model=ResponseBasic,
            status_code=200,
            summary=f"Update a single hook object"
            )
@HttpErrorHandler()
async def update(
                model_payload: Hook,
                request: Request,
                object_id: Optional[str] = None
                ):
    cmdboss = CMDBOSS_db()
    result = cmdboss.update(model_instance_data=model_payload, object_id=object_id, path=f"{request.url}")
    return jsonable_encoder(result)
