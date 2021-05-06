
from pydantic import Field, BaseModel
from datetime import datetime


class cmdboss_base_model(BaseModel):
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)
