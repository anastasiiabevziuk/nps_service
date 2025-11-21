import os
from dotenv import load_dotenv
import asyncpg
from typing import Optional

load_dotenv()


pool: Optional[asyncpg.Pool] = None


DSN = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)


async def connect_to_db():
    """Create pool connection to PostgreSQL."""
    global pool
    print("Connecting to PostgreSQL...")
    try:
        pool = await asyncpg.create_pool(DSN)
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
    """Return global connection pool. Used in FastAPI dependencies."""
    if pool is None:
        raise ConnectionError("Connection pool asyncpg is not initialized.")
    return pool
