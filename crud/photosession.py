import asyncpg
from typing import Dict, Any, List, Optional


# --- CREATE (POST) ---
async def create_photosession(
    db_pool: asyncpg.Pool, new_data: Dict[str, Any]
) -> Dict[str, Any]:
    query = """
        INSERT INTO "HR".PHOTOSESSION 
            (model_id, photographer_id, location, rating)
        VALUES 
            ($1, $2, $3, $4)
        RETURNING photosession_id, model_id, photographer_id, location, rating;
    """
    record = await db_pool.fetchrow(
        query,
        new_data["model_id"],
        new_data["photographer_id"],
        new_data.get("location"),
        new_data.get("rating"),
    )
    return dict(record)


# --- READ ALL (GET /photosession/) ---
async def get_all_photosessions(db_pool: asyncpg.Pool) -> List[Dict[str, Any]]:
    query = 'SELECT photosession_id, model_id, photographer_id, location, rating FROM "HR".PHOTOSESSION;'
    records = await db_pool.fetch(query)
    return [dict(record) for record in records]


# --- READ ONE (GET /photosession/{id}) ---
async def get_photosession_by_id(
    db_pool: asyncpg.Pool, photosession_id: int
) -> Optional[Dict[str, Any]]:
    query = 'SELECT photosession_id, model_id, photographer_id, location, rating FROM "HR".PHOTOSESSION WHERE photosession_id = $1;'
    record = await db_pool.fetchrow(query, photosession_id)
    return dict(record) if record else None


# --- UPDATE (PUT) ---
async def update_photosession_by_id(
    db_pool: asyncpg.Pool, photosession_id: int, new_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    query = """
        UPDATE "HR".PHOTOSESSION
        SET 
            model_id = $2, 
            photographer_id = $3, 
            location = $4, 
            rating = $5
        WHERE photosession_id = $1
        RETURNING photosession_id, model_id, photographer_id, location, rating;
    """
    record = await db_pool.fetchrow(
        query,
        photosession_id,
        new_data["model_id"],
        new_data["photographer_id"],
        new_data.get("location"),
        new_data.get("rating"),
    )
    return dict(record) if record else None


# --- DELETE ---
async def delete_photosession_by_id(db_pool: asyncpg.Pool, photosession_id: int) -> int:

    query = 'DELETE FROM "HR".PHOTOSESSION WHERE photosession_id = $1;'
    status = await db_pool.execute(query, photosession_id)
    return int(status.split()[-1])
