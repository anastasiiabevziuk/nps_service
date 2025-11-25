import asyncpg
from fastapi import HTTPException, status
from typing import Dict, Any, List


from crud.photo import (
    create_photo,
    get_all_photos,
    get_photo_by_id,
    update_photo_by_id,
    delete_photo_by_id,
)
from schemas.photo import PhotoResponse


# --- CREATE ---
async def create_photo_service(
    db_pool: asyncpg.Pool, new_data: Dict[str, Any]
) -> PhotoResponse:
    try:
        data_for_db = new_data.copy()

        iso_value = data_for_db.get("iso")
        if iso_value is not None:
            try:

                data_for_db["iso"] = int(iso_value)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"ISO value '{iso_value}' must be a valid integer, as defined in the database schema.",
                )

        created_photo = await create_photo(db_pool, data_for_db)

        return PhotoResponse(**created_photo)

    except asyncpg.exceptions.ForeignKeyViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Photosession ID does not exist. Cannot create photo.",
        )

    except Exception as e:

        if isinstance(e, HTTPException):
            raise e

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while creating photo: {e}",
        )


# --- READ ALL ---
async def get_all_photos_service(db_pool: asyncpg.Pool) -> List[PhotoResponse]:
    try:
        photos = await get_all_photos(db_pool)
        return [PhotoResponse(**photo) for photo in photos]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while fetching all photos: {e}",
        )


# --- READ ONE ---
async def get_photo_by_id_service(
    db_pool: asyncpg.Pool, photo_id: int
) -> PhotoResponse:
    try:
        photo = await get_photo_by_id(db_pool, photo_id)
        if photo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Photo with id {photo_id} not found.",
            )
        return PhotoResponse(**photo)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while fetching photo by ID: {e}",
        )


# --- UPDATE ---
async def update_photo_service(
    db_pool: asyncpg.Pool, photo_id: int, new_data: Dict[str, Any]
) -> PhotoResponse:
    try:
        updated_photo = await update_photo_by_id(
            db_pool, photo_id, new_data.model_dump()
        )
        if updated_photo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Photo with id {photo_id} not found for update.",
            )
        return PhotoResponse(**updated_photo)
    except asyncpg.exceptions.ForeignKeyViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Photosession ID does not exist. Cannot update photo.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while updating photo by ID: {e}",
        )


# --- DELETE ---
async def delete_photo_service(db_pool: asyncpg.Pool, photo_id: int) -> Dict[str, str]:
    try:
        deleted_count = await delete_photo_by_id(db_pool, photo_id)
        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Photo with id {photo_id} not found for deletion.",
            )
        return {
            "status": "success",
            "message": f"Photo with id {photo_id} successfully deleted.",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while deleting photo by ID: {e}",
        )
