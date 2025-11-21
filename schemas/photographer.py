from pydantic import BaseModel
from typing import Optional


class PhotographerBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    camera: Optional[str] = None
    rating: Optional[int] = None

    class Config:
        from_attributes = True


class PhotographerResponse(PhotographerBase):
    photographer_id: int
