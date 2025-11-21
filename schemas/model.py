from pydantic import BaseModel
from typing import Optional


class ModelBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str

    class Config:
        from_attributes = True


class ModelResponse(ModelBase):
    model_id: int
