from fastapi import (
    APIRouter,
    Depends,
    Path,
    status,
    UploadFile,
    File,
    Form,
    HTTPException,
)
import asyncpg
from typing import Dict, Any, List


from database import get_db_pool
from services.photo import (
    create_photo_service,
    get_all_photos_service,
    get_photo_by_id_service,
    update_photo_service,
    delete_photo_service,
)


from schemas.photo import PhotoResponse
import shutil
import os

from services.exif_reader import get_exif_data


UPLOAD_DIR = "uploaded_photos"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


router = APIRouter(prefix="/photo", tags=["Photo"])


# --- POST (Create Photo with File Upload) ---
@router.post("/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
async def photo_create(
    file: UploadFile = File(..., description="Photo file to upload"),
    photosession_id: int = Form(
        ..., description="ID of the photo session to which the photo belongs"
    ),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> PhotoResponse:

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{photosession_id}_{os.urandom(8).hex()}{file_extension}"
    temp_file_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:

        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        exif_data = get_exif_data(temp_file_path)

        new_data = {
            "photosession_id": photosession_id,
            "camera": exif_data.get("camera", "Unknown"),
            "iso": exif_data.get("iso", None),
            "lens": exif_data.get("LensModel", None),
            "file_path": temp_file_path,
        }

        created_photo = await create_photo_service(db_pool, new_data)

        return created_photo

    except Exception as e:

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(
            status_code=500, detail=f"Failed to process or save file: {e}"
        )


# --- GET ALL (Read All Photos) ---
@router.get("/", response_model=List[PhotoResponse])
async def photo_read_all(
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> List[PhotoResponse]:
    """Get a list of all photos."""
    return await get_all_photos_service(db_pool)


# --- GET BY ID (Read One Photo) ---
@router.get("/{photo_id}", response_model=PhotoResponse)
async def photo_read_one(
    photo_id: int = Path(..., description="The ID of the photo to retrieve"),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> PhotoResponse:
    """Get a photo record by its ID."""
    return await get_photo_by_id_service(db_pool, photo_id)


# --- PUT (Update Photo) ---
@router.put("/{photo_id}", response_model=PhotoResponse)
async def photo_update(
    photo_data: Dict[str, Any],
    photo_id: int = Path(..., description="The ID of the photo to update"),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> PhotoResponse:
    """Update an existing 'photo' record."""
    return await update_photo_service(db_pool, photo_id, photo_data)


# --- DELETE (Delete Photo) ---
@router.delete("/{photo_id}", status_code=status.HTTP_200_OK)
async def photo_delete(
    photo_id: int = Path(..., description="The ID of the photo to delete"),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> Dict[str, str]:
    """Delete a 'photo' record by its ID."""
    return await delete_photo_service(db_pool, photo_id)
