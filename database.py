import os
from dotenv import load_dotenv
import asyncpg
from typing import Optional

load_dotenv()

pool: Optional[asyncpg.Pool] = None


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
        f"{os.getenv('POSTGRES_PORT', 5432)}/"
        f"{os.getenv('POSTGRES_DB')}"
    )


async def connect_to_db():
    """Create pool connection to PostgreSQL."""
    global pool
    print(f"Connecting to PostgreSQL at {DATABASE_URL.split('@')[-1]}...")
    try:
        pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        print("✅ Connection pool created successfully.")
    except Exception as e:
        print(f"❌ Error creating connection pool: {e}")


async def close_db_connection():
    """Close connection pool to PostgreSQL."""
    global pool
    if pool:
        await pool.close()
        print("🛑 Connection pool to PostgreSQL closed.")


def get_db_pool() -> asyncpg.Pool:
    """Return global connection pool."""
    if pool is None:
        raise ConnectionError("Connection pool asyncpg is not initialized.")
    return pool
