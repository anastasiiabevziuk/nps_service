from pydantic import BaseModel
from typing import Optional, List


class PhotosessionBase(BaseModel):
    model_id: int
    photographer_id: int
    location: Optional[str] = None
    rating: Optional[int] = None

    class Config:
        from_attributes = True


class PhotosessionResponse(PhotosessionBase):
    photosession_id: int
