from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta, timezone
import json
import logging

from .settings import settings as auth_settings
from ..core.settings import settings as app_settings
from .models import User
from .service import Service as AuthService
from ..dependencies import get_current_user
from .schemas import TokensResponse, AuthRequest


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/auth',
    tags=['authorization']
)


@router.post("/login", response_model=TokensResponse, status_code=201)
async def login_via_telegram(data: AuthRequest):

    payload = AuthService.validate_init_data(data.init_data)
    user_info = json.loads(payload['user'])
    user, _ = await User.get_or_create(
        telegram_id = user_info['id'],
        defaults= { ... },
    )

    access_token, access_expires_at = AuthService.create_jwt(data={"sub": user.id, "token_type":"access"})
    refresh_token, refresh_expires_at = AuthService.create_jwt(data={"sub": user.id, "token_type":"refresh"})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "access_token_expire": access_expires_at,
        "refresh_token_expire": refresh_expires_at
    }