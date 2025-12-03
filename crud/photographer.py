import asyncpg
from typing import Dict, Any, List, Optional


# --- CREATE (POST) ---
async def create_photographer(
    db_pool: asyncpg.Pool, new_data: Dict[str, Any]
) -> Dict[str, Any]:
    query = """
        INSERT INTO "HR".PHOTOGRAPHER 
            (first_name, last_name, phone, email, camera, rating)
        VALUES 
            ($1, $2, $3, $4, $5, $6)
        RETURNING photographer_id, first_name, last_name, phone, email, camera, rating;
    """
    record = await db_pool.fetchrow(
        query,
        new_data["first_name"],
        new_data["last_name"],
        new_data["phone"],
        new_data["email"],
        new_data.get("camera"),
        new_data.get("rating"),
    )
    return dict(record)


# --- READ ALL (GET /photographer/) ---
async def get_all_photographers(
    db_pool: asyncpg.Pool, sort_by: Optional[str] = None
) -> List[Dict[str, Any]]:
    query = 'SELECT photographer_id, first_name, last_name, phone, email, camera, rating FROM "HR".PHOTOGRAPHER '
    if sort_by == "rating_asc":
        query += " ORDER BY rating ASC"
    elif sort_by == "rating_desc":
        query += " ORDER BY rating DESC"
    records = await db_pool.fetch(query)
    return [dict(record) for record in records]


# --- READ ONE (GET /photographer/{id}) ---
async def get_photographer_by_id(
    db_pool: asyncpg.Pool, photographer_id: int
) -> Optional[Dict[str, Any]]:
    query = 'SELECT photographer_id, first_name, last_name, phone, email, camera, rating FROM "HR".PHOTOGRAPHER WHERE photographer_id = $1;'
    record = await db_pool.fetchrow(query, photographer_id)
    return dict(record) if record else None


# --- UPDATE (PUT) ---
async def update_photographer_by_id(
    db_pool: asyncpg.Pool, photographer_id: int, new_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    query = """
        UPDATE "HR".PHOTOGRAPHER
        SET 
            first_name = $2, 
            last_name = $3, 
            phone = $4, 
            email = $5,
            camera = $6,
            rating = $7
        WHERE photographer_id = $1
        RETURNING photographer_id, first_name, last_name, phone, email, camera, rating;
    """
    record = await db_pool.fetchrow(
        query,
        photographer_id,
        new_data["first_name"],
        new_data["last_name"],
        new_data["phone"],
        new_data["email"],
        new_data.get("camera"),
        new_data.get("rating"),
    )
    return dict(record) if record else None


# --- DELETE ---
async def delete_photographer_by_id(db_pool: asyncpg.Pool, photographer_id: int) -> int:
    query = 'DELETE FROM "HR".PHOTOGRAPHER WHERE photographer_id = $1;'
    status = await db_pool.execute(query, photographer_id)
    return int(status.split()[-1])
