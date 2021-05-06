from typing import Optional, List
from enum import Enum
from pydantic import BaseModel


class StatusEnum(str, Enum):
    success = "success"
    error = "error"


class ResponseBasic(BaseModel):
    status: StatusEnum
    result: list


class SysModelIngest(BaseModel):
    base64_payload: str
    name: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "base64_payload": "ZnJvbSBweWRhbnRpYyBpbXBvcnQgQmFzZU1vZGVsCgpjbGFzcyBkZXZpY2UoQmFzZU1vZGVsKToKICAgIG5hbWU6IHN0cg=="
            }
        }


class CMDBOSSQuery(BaseModel):
    filter: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "filter": {
                    "name": "bob"
                }
            }
        }


class HookEvent(str, Enum):
    create = "create"
    retrieve = "retrieve"
    update = "update"
    delete = "delete"


class HookModelArgs(BaseModel):
    model: Optional[str] = None
    order: int
    operation: HookEvent
    filter: Optional[dict] = None


class Hook(BaseModel):
    name: str
    base64_payload: str
    events: List[HookModelArgs]
