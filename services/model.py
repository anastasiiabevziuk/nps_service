import asyncpg
from fastapi import HTTPException
from typing import List, Dict, Any
from schemas.model import ModelBase, ModelResponse

from crud.model import (
    get_all_models,
    get_model_by_id,
    delete_model_by_id,
    update_model_by_id,
    create_model,
)


# --- READ ALL ---
async def get_models_service(db_pool: asyncpg.Pool) -> List[Dict[str, Any]]:
    try:
        models_data = await get_all_models(db_pool)

        return models_data

    except Exception as e:

        raise HTTPException(
            status_code=500, detail=f"Database error while retrieving models: {e}"
        )


# --- READ ONE ---
async def get_model_by_id_service(
    db_pool: asyncpg.Pool, model_id: int
) -> Dict[str, Any]:

    try:
        model_data = await get_model_by_id(db_pool, model_id)

        if model_data is None:

            raise HTTPException(
                status_code=404, detail=f"Model with id {model_id} not found"
            )

        return model_data

    except Exception as e:

        if isinstance(e, HTTPException):
            raise e

        raise HTTPException(
            status_code=500, detail=f"Database error while retrieving model by ID: {e}"
        )


# --- DELETE ---
async def delete_model_service(db_pool: asyncpg.Pool, model_id: int) -> Dict[str, str]:

    try:
        deleted_count = await delete_model_by_id(db_pool, model_id)

        if deleted_count == 0:
            raise HTTPException(
                status_code=404, detail=f"Model with id {model_id} not found"
            )

        return {
            "status": "success",
            "message": f"Model with id {model_id} successfully deleted",
        }

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e

        raise HTTPException(
            status_code=500, detail=f"Database error while deleting model by ID: {e}"
        )


# --- UPDATE ---
async def update_model_service(
    db_pool: asyncpg.Pool, model_id: int, new_data: Dict[str, Any]
) -> Dict[str, Any]:

    try:

        updated_model = await update_model_by_id(db_pool, model_id, new_data)

        if updated_model is None:

            raise HTTPException(
                status_code=404, detail=f"Model with id {model_id} not found for update"
            )

        return updated_model

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e

        raise HTTPException(
            status_code=500, detail=f"Database error while updating model by ID: {e}"
        )


# --- CREATE ---
async def create_model_service(
    db_pool: asyncpg.Pool, new_data: ModelBase
) -> ModelResponse:

    try:

        created_model = await create_model(db_pool, new_data)

        return created_model

    except asyncpg.exceptions.UniqueViolationError:

        raise HTTPException(
            status_code=400,
            detail="A model with this unique data (e.g., email or phone) already exists",
        )
    except Exception as e:

        raise HTTPException(
            status_code=500, detail=f"Database error while creating model: {e}"
        )
