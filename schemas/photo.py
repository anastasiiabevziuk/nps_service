from pydantic import BaseModel, Field
from typing import Optional
from fastapi import UploadFile


class PhotoUploadRequest(BaseModel):
    photosession_id: int = Field(
        ..., description="ID of the photosession this photo belongs to"
    )


class PhotoResponse(BaseModel):
    photo_id: int
    photosession_id: int
    camera: str
    file_path: str
    lens: Optional[str] = None
    iso: Optional[int] = None

    class Config:
        from_attributes = True
