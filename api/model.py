from fastapi import Depends, Path, status, APIRouter
import asyncpg
from database import get_db_pool
from typing import List, Dict, Any

from services.model import (
    get_models_service,
    get_model_by_id_service,
    delete_model_service,
    update_model_service,
    create_model_service,
)


from schemas.model import ModelBase, ModelResponse


router = APIRouter(prefix="/model", tags=["Model"])


# --- GET ALL (Read All Models) ---
@router.get("/")
async def model_list(
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> List[Dict[str, Any]]:
    """
    Gets all records from the 'model' table via the service layer.
    """

    return await get_models_service(db_pool)


# --- GET BY ID (Read One Model) ---
@router.get("/{model_id}", response_model=ModelResponse)
async def model_details(
    model_id: int = Path(..., description="The ID of the model to retrieve"),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> Dict[str, Any]:

    return await get_model_by_id_service(db_pool, model_id)


# --- DELETE (Delete Model) ---
@router.delete("/{model_id}", status_code=status.HTTP_200_OK)
async def model_delete(
    model_id: int = Path(..., description="The ID of the model to delete"),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> Dict[str, str]:

    return await delete_model_service(db_pool, model_id)


# --- PUT (Update Model) ---
@router.put("/{model_id}", response_model=ModelResponse)
async def model_update(
    model_data: ModelBase,
    model_id: int = Path(..., description="The ID of the model to update"),
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> Dict[str, Any]:

    return await update_model_service(db_pool, model_id, model_data.model_dump())


# --- POST (Create Model) ---
@router.post("/", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
async def model_create(
    model_data: ModelBase,
    db_pool: asyncpg.Pool = Depends(get_db_pool),
) -> Dict[str, Any]:

    return await create_model_service(db_pool, model_data.model_dump())
