import asyncpg
from typing import Dict, Any, List, Optional


# --- CREATE (POST) ---
async def create_photo(
    db_pool: asyncpg.Pool, new_data: Dict[str, Any]
) -> Dict[str, Any]:
    query = """
        INSERT INTO "HR".PHOTO 
            (photosession_id, camera, file_path, lens, iso)
        VALUES 
            ($1, $2, $3, $4, $5)
        RETURNING photo_id, photosession_id, camera, file_path, lens, iso;
    """
    record = await db_pool.fetchrow(
        query,
        new_data["photosession_id"],
        new_data["camera"],
        new_data["file_path"],
        new_data.get("lens"),
        new_data.get("iso"),
    )
    return dict(record)


# --- READ ALL (GET /photo/) ---
async def get_all_photos(db_pool: asyncpg.Pool) -> List[Dict[str, Any]]:
    query = 'SELECT photo_id, photosession_id, camera, file_path, lens, iso FROM "HR".PHOTO;'

    records = await db_pool.fetch(query)
    return [dict(record) for record in records]


# --- READ ONE (GET /photo/{id}) ---
async def get_photo_by_id(
    db_pool: asyncpg.Pool, photo_id: int
) -> Optional[Dict[str, Any]]:
    query = 'SELECT photo_id, photosession_id, camera, file_path, lens, iso FROM "HR".PHOTO WHERE photo_id = $1;'
    record = await db_pool.fetchrow(query, photo_id)
    return dict(record) if record else None


# --- UPDATE (PUT) ---
async def update_photo_by_id(
    db_pool: asyncpg.Pool, photo_id: int, new_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    query = """
        UPDATE "HR".PHOTO
        SET 
            photosession_id = $2, 
            camera = $3, 
            file_path = $4, 
            lens = $5,
            iso = $6
        WHERE photo_id = $1
        RETURNING photo_id, photosession_id, camera, file_path, lens, iso;
    """
    record = await db_pool.fetchrow(
        query,
        photo_id,
        new_data["photosession_id"],
        new_data["camera"],
        new_data["file_path"],
        new_data.get("lens"),
        new_data.get("iso"),
    )
    return dict(record) if record else None


# --- DELETE ---
async def delete_photo_by_id(db_pool: asyncpg.Pool, photo_id: int) -> int:
    query = 'DELETE FROM "HR".PHOTO WHERE photo_id = $1;'
    status = await db_pool.execute(query, photo_id)
    return int(status.split()[-1])
