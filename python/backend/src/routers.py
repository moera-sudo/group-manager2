from fastapi import APIRouter
from datetime import datetime, timedelta, timezone
import logging


from .auth.router import router as AuthRouter

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api", tags=['api'])


@router.get("/ping")
async def ping_response():
    logger.info("Request to server")
    pong = "pong"
    now = datetime.now(timezone.utc)

    return {
        "pong":pong,
        "time":now
    }

router.include_router(AuthRouter)