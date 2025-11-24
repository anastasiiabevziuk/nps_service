from fastapi import APIRouter, Depends, Path, status
import asyncpg
from typing import Dict, Any, List

from database import get_db_pool
from services.photosession import (
    create_photosession_service,
    get_all_photosessions_service,
    get_photosession_by_id_service,
    update_photosession_service,
    delete_photosession_service,
)
from schemas.photosession import PhotosessionBase, PhotosessionResponse


router = APIRouter(prefix="/photosession", tags=["Photosession"])


# --- POST (Create Photosession) ---
@router.post(
    "/", response_model=PhotosessionResponse, status_code=status.HTTP_201_CREATED
)
async def photosession_create(
    ps_data: PhotosessionBase,
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> PhotosessionResponse:
    """Create new 'photosession'."""
    return await create_photosession_service(db_pool, ps_data)


# --- GET ALL (Read All Photosessions) ---
@router.get("/", response_model=List[PhotosessionResponse])
async def photosession_read_all(
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> List[PhotosessionResponse]:
    """Get a list of all photosessions."""
    return await get_all_photosessions_service(db_pool)


# --- GET BY ID (Read One Photosession) ---
@router.get("/{photosession_id}", response_model=PhotosessionResponse)
async def photosession_read_one(
    photosession_id: int = Path(
        ..., description="The ID of the photosession to retrieve"
    ),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> PhotosessionResponse:
    """Get a photosession record by its ID."""
    return await get_photosession_by_id_service(db_pool, photosession_id)


# --- PUT (Update Photosession) ---
@router.put("/{photosession_id}", response_model=PhotosessionResponse)
async def photosession_update(
    ps_data: PhotosessionBase,
    photosession_id: int = Path(
        ..., description="The ID of the photosession to update"
    ),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> PhotosessionResponse:
    """Update an existing 'photosession' record."""
    return await update_photosession_service(db_pool, photosession_id, ps_data)


# --- DELETE (Delete Photosession) ---
@router.delete("/{photosession_id}", status_code=status.HTTP_200_OK)
async def photosession_delete(
    photosession_id: int = Path(
        ..., description="The ID of the photosession to delete"
    ),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> Dict[str, str]:
    """Delete a photosession record by its ID."""
    return await delete_photosession_service(db_pool, photosession_id)
