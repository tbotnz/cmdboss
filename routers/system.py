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
from backend.util.file_mgr import FileMgr

log = logging.getLogger(__name__)

router = APIRouter()
filemgr = FileMgr()

@router.get("/models/{model_name}", response_model=ResponseBasic, status_code=200)
@HttpErrorHandler()
async def retrieve_model(model_name: str):
    payload = {}
    payload["name"] = model_name
    payload["route_type"] = "model"
    result = filemgr.retrieve_file(payload)
    return jsonable_encoder(result)

@router.post("/models/{model_name}", response_model=ResponseBasic, status_code=201)
@HttpErrorHandler()
async def create_model(model_payload: SysModelIngest, model_name: str):
    payload = model_payload.dict(exclude_none=True)
    payload["name"] = model_name
    payload["route_type"] = "model"
    result = filemgr.create_file(payload)
    # reload_routes()
    return jsonable_encoder(result)

@router.delete("/models/{model_name}", status_code=204)
@HttpErrorHandler()
async def delete_model(model_name: str):
    payload = {}
    payload["name"] = model_name
    payload["route_type"] = "model"
    result = filemgr.delete_file(payload)
    # reload_routes()
    return jsonable_encoder(result)

@router.get("/models/", response_model=ResponseBasic, status_code=200)
@HttpErrorHandler()
async def retrieve_models():
    payload = {}
    payload["route_type"] = "model"
    result = filemgr.retrieve_files(payload)
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
