import asyncpg
from fastapi import HTTPException, status
from typing import Dict, Any, List


from crud.photographer import (
    create_photographer,
    get_all_photographers,
    get_photographer_by_id,
    update_photographer_by_id,
    delete_photographer_by_id,
)

from schemas.photographer import PhotographerBase, PhotographerResponse


# --- CREATE ---
async def create_photographer_service(
    db_pool: asyncpg.Pool, new_data: PhotographerBase
) -> PhotographerResponse:
    try:
        created_ph = await create_photographer(db_pool, new_data.model_dump())
        return PhotographerResponse(**created_ph)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A photographer with this email or phone already exists.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while creating photographer: {e}",
        )


# --- READ ALL ---
async def get_all_photographers_service(
    db_pool: asyncpg.Pool,
) -> List[PhotographerResponse]:
    try:
        photographers = await get_all_photographers(db_pool)
        return [PhotographerResponse(**ph) for ph in photographers]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while fetching all photographers: {e}",
        )


# --- READ ONE ---
async def get_photographer_by_id_service(
    db_pool: asyncpg.Pool, photographer_id: int
) -> PhotographerResponse:
    try:
        photographer = await get_photographer_by_id(db_pool, photographer_id)
        if photographer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Photographer with id {photographer_id} not found.",
            )
        return PhotographerResponse(**photographer)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while fetching photographer by ID: {e}",
        )


# --- UPDATE ---
async def update_photographer_service(
    db_pool: asyncpg.Pool, photographer_id: int, new_data: PhotographerBase
) -> PhotographerResponse:
    try:
        updated_ph = await update_photographer_by_id(
            db_pool, photographer_id, new_data.model_dump()
        )
        if updated_ph is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Photographer with id {photographer_id} not found for update.",
            )
        return PhotographerResponse(**updated_ph)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while updating photographer by ID: {e}",
        )


# --- DELETE ---
async def delete_photographer_service(
    db_pool: asyncpg.Pool, photographer_id: int
) -> Dict[str, str]:
    try:
        deleted_count = await delete_photographer_by_id(db_pool, photographer_id)
        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Photographer with id {photographer_id} not found for deletion.",
            )
        return {
            "status": "success",
            "message": f"Photographer with id {photographer_id} successfully deleted.",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while deleting photographer by ID: {e}",
        )
