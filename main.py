from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncpg
from database import connect_to_db, close_db_connection

from api.model import router as model_router
from api.photographer import router as photographer_router
from api.photosession import router as photosession_router
from api.photo import router as photo_router
from auth.router import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle event handler (Lifespan Events).

    1. Logic executed on startup.
    """
    await connect_to_db()

    yield

    await close_db_connection()


app = FastAPI(
    title="API NPS Service",
    description="It is API for managing models, photographers, their sessions, and photos. Data is stored in PostgreSQL.",
    version="1.0.0",
    contact={
        "name": "Anastasiia (Developer)",
        "email": "anastasiiabevziuk@gmail.com",
    },
    # --- END КЛЮЧОВІ ПОЛЯ ---
    lifespan=lifespan,
)

app.include_router(model_router)
app.include_router(photographer_router)
app.include_router(photosession_router)
app.include_router(photo_router)
app.include_router(auth_router)
