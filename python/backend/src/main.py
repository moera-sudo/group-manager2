from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from tortoise import Tortoise
import uvicorn
import logging

from .core.settings import settings
from .core.config import TORTOISE_ORM, setup_logging
from .routers import router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    setup_logging(debug=settings.DEBUG)

    logger.info("Starting application initialization")
    await Tortoise.init(config=TORTOISE_ORM)
    logger.info("Tortoise-ORM connection established")

    if settings.DEBUG:
        logger.info("DEBUG mode is on. Starting generate schemas ")
        await Tortoise.generate_schemas()
        logger.info("Schemas generated")

    logger.info("Application startup complete")
    yield

    logger.info("Shutting down application")
    await Tortoise.close_connections()
    logger.info("Database connection closed.")
    logger.info("Application shutdown complete")


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESC,
    version=settings.APP_VERSION,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)
