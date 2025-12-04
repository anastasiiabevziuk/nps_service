from fastapi import Depends, Path, status, APIRouter, Query
import asyncpg
from database import get_db_pool
from typing import List, Dict, Optional
from auth.router import get_current_user
from auth.schemas import UserInDB

from services.photographer import (
    create_photographer_service,
    get_all_photographers_service,
    get_photographer_by_id_service,
    update_photographer_service,
    delete_photographer_service,
)


from schemas.photographer import PhotographerBase, PhotographerResponse


router = APIRouter(prefix="/photographer", tags=["Photographer"])


# --- POST (Create Photographer) ---
@router.post(
    "/",
    response_model=PhotographerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def photographer_create(
    ph_data: PhotographerBase,
    current_user: UserInDB = Depends(get_current_user),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> PhotographerResponse:
    """
    Create 'photographer'.
    """
    return await create_photographer_service(db_pool, ph_data)


# --- GET ALL (Read All Photographers) ---
@router.get("/", response_model=List[PhotographerResponse])
async def photographer_read_all(
    sort: Optional[str] = Query(
        None, description="Sort. Use 'rating_asc' or 'rating_desc'."
    ),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> List[PhotographerResponse]:

    photographers = await get_all_photographers_service(db_pool, sort_by=sort)
    return photographers


# --- GET BY ID (Read One Photographer) ---
@router.get("/{photographer_id}", response_model=PhotographerResponse)
async def photographer_read_one(
    photographer_id: int = Path(
        ..., description="The ID of the photographer to retrieve"
    ),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> PhotographerResponse:
    """
    Gets a 'photographer' record by its ID.
    """
    return await get_photographer_by_id_service(db_pool, photographer_id)


# --- PUT (Update Photographer) ---
@router.put("/{photographer_id}", response_model=PhotographerResponse)
async def photographer_update(
    ph_data: PhotographerBase,
    photographer_id: int = Path(
        ..., description="The ID of the photographer to update"
    ),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> PhotographerResponse:
    """
    Updates an existing 'photographer' record by its ID.
    """
    return await update_photographer_service(db_pool, photographer_id, ph_data)


# --- DELETE (Delete Photographer) ---
@router.delete("/{photographer_id}", status_code=status.HTTP_200_OK)
async def photographer_delete(
    photographer_id: int = Path(
        ..., description="The ID of the photographer to delete"
    ),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> Dict[str, str]:
    """
    Deletes a 'photographer' record by its ID.
    """
    return await delete_photographer_service(db_pool, photographer_id)
