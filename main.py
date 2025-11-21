from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncpg
from database import connect_to_db, close_db_connection

from api.model import router as model_router
from api.photographer import router as photographer_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle event handler (Lifespan Events).

    1. Logic executed on startup.
    """
    await connect_to_db()

    yield

    await close_db_connection()


app = FastAPI(lifespan=lifespan)


app.include_router(model_router)
app.include_router(photographer_router)
