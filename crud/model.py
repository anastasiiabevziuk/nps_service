import asyncpg
from typing import List, Dict, Any, Optional


# --- READ ALL (GET /model/) ---
async def get_all_models(db_pool: asyncpg.Pool) -> List[Dict[str, Any]]:

    query = 'SELECT model_id, first_name, last_name, phone, email FROM "HR".model;'

    records = await db_pool.fetch(query)

    return [dict(r) for r in records]


# --- READ ONE (GET /model/{id}) ---
async def get_model_by_id(
    db_pool: asyncpg.Pool, model_id: int
) -> Optional[Dict[str, Any]]:

    query = """
        SELECT model_id, first_name, last_name, phone, email 
        FROM "HR".model
        WHERE model_id = $1;
    """

    record = await db_pool.fetchrow(query, model_id)

    if record:
        return dict(record)
    else:
        return None


# --- DELETE ---
async def delete_model_by_id(db_pool: asyncpg.Pool, model_id: int) -> int:

    query = """
        DELETE FROM "HR".model
        WHERE model_id = $1;
    """

    status = await db_pool.execute(query, model_id)

    try:
        deleted_count = int(status.split()[-1])
        return deleted_count
    except (ValueError, IndexError):
        return 0


# --- UPDATE (PUT) ---
async def update_model_by_id(
    db_pool: asyncpg.Pool, model_id: int, new_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:

    query = """
        UPDATE "HR".model
        SET 
            first_name = $2, 
            last_name = $3, 
            phone = $4, 
            email = $5
        WHERE model_id = $1
        RETURNING model_id, first_name, last_name, phone, email; -- RETURNING 
    """

    record = await db_pool.fetchrow(
        query,
        model_id,
        new_data["first_name"],
        new_data["last_name"],
        new_data["phone"],
        new_data["email"],
    )

    if record:
        return dict(record)
    else:
        return None


import asyncpg
from typing import Dict, Any, Optional


# --- CREATE (POST) ---
async def create_model(
    db_pool: asyncpg.Pool, new_data: Dict[str, Any]
) -> Dict[str, Any]:

    query = """
        INSERT INTO "HR".model 
            (first_name, last_name, phone, email)
        VALUES 
            ($1, $2, $3, $4)
        RETURNING model_id, first_name, last_name, phone, email; 
    """

    record = await db_pool.fetchrow(
        query,
        new_data["first_name"],
        new_data["last_name"],
        new_data["phone"],
        new_data["email"],
    )

    return dict(record)
