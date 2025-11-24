import asyncpg
from fastapi import HTTPException, status
from typing import Dict, Any, List


from crud.photosession import (
    create_photosession,
    get_all_photosessions,
    get_photosession_by_id,
    update_photosession_by_id,
    delete_photosession_by_id,
)
from schemas.photosession import PhotosessionBase, PhotosessionResponse


# --- CREATE ---
async def create_photosession_service(
    db_pool: asyncpg.Pool, new_data: PhotosessionBase
) -> PhotosessionResponse:
    try:
        created_ps = await create_photosession(db_pool, new_data.model_dump())
        return PhotosessionResponse(**created_ps)
    except asyncpg.exceptions.ForeignKeyViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model ID or Photographer ID does not exist. Cannot create photosession.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while creating photosession: {e}",
        )


# --- READ ALL ---
async def get_all_photosessions_service(
    db_pool: asyncpg.Pool,
) -> List[PhotosessionResponse]:
    try:
        sessions = await get_all_photosessions(db_pool)
        return [PhotosessionResponse(**ps) for ps in sessions]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while fetching all photosessions: {e}",
        )


# --- READ ONE ---
async def get_photosession_by_id_service(
    db_pool: asyncpg.Pool, photosession_id: int
) -> PhotosessionResponse:
    try:
        session = await get_photosession_by_id(db_pool, photosession_id)
        if session is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Photosession with id {photosession_id} not found.",
            )
        return PhotosessionResponse(**session)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while fetching photosession by ID: {e}",
        )


# --- UPDATE ---
async def update_photosession_service(
    db_pool: asyncpg.Pool, photosession_id: int, new_data: PhotosessionBase
) -> PhotosessionResponse:
    try:
        updated_ps = await update_photosession_by_id(
            db_pool, photosession_id, new_data.model_dump()
        )
        if updated_ps is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Photosession with id {photosession_id} not found for update.",
            )
        return PhotosessionResponse(**updated_ps)
    except asyncpg.exceptions.ForeignKeyViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model ID or Photographer ID does not exist. Cannot update photosession.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while updating photosession by ID: {e}",
        )


# --- DELETE ---
async def delete_photosession_service(
    db_pool: asyncpg.Pool, photosession_id: int
) -> Dict[str, str]:
    try:
        deleted_count = await delete_photosession_by_id(db_pool, photosession_id)
        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Photosession with id {photosession_id} not found for deletion.",
            )
        return {
            "status": "success",
            "message": f"Photosession with id {photosession_id} successfully deleted.",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while deleting photosession by ID: {e}",
        )
