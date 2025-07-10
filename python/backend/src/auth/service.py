import urllib.parse
from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from typing import Optional
from datetime import timedelta, datetime, timezone
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist
import hashlib
import hmac
import urllib

from .schemas import TokenData, Token
from .settings import settings as settings
from ..core.settings import settings as app_setting
from .models import User


class Service:

    @staticmethod
    def create_jwt(data: TokenData, expires_delta: Optional[timedelta] = None) -> str:
        try:
            to_encode = data.model_dump(exclude_unset=True)
            to_encode['sub_tg'] = str(to_encode['sub_tg'])

            now = datetime.now(timezone.utc)

            if data.token_type == "refresh":
                expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE)
            elif data.token_type == "access" and expires_delta:
                expire = now + expires_delta
            elif data.token_type == "access" and not expires_delta:
                expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPRIRE)

            to_encode.update({
                'exp': expire,
                'iat': now,
                'token_type': data.token_type
            })

            
        except (ValueError, ValidationError) as e:
            HTTPException(
                status_code=500,
                detail=f'Token Data error:{e}'
            )
        except Exception as e:
            HTTPException(
                status_code=500,
                detail=f"Failed to prepare payload: {e}"
            )
        
        else:
            try:
                secret_key = settings.SECRET_KEY if data.token_type == "access" else settings.REFRESH_SECRET_KEY

                payload = jwt.encode(
                    to_encode,
                    secret_key,
                    algorithm=settings.ALGORITHM
                )

                return (payload, expire)
            except Exception as e:
                HTTPException(
                    status_code=500,
                    detail=f"Failed to create jwt Token:{e}"
                )

    @staticmethod
    def decode_jwt(data: Token) -> Optional[TokenData]:
        try:

            secret_key = settings.SECRET_KEY if data.token_type == 'access' else settings.REFRESH_SECRET_KEY

            payload = jwt.decode(
                data.token,
                secret_key,
                algorithms=settings.ALGORITHM
            )

            token_data = TokenData(**payload)

            token_data.sub_tg = int(token_data.sub_tg)
 
            return token_data
        
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail='Token expired'
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to decode Token: {e}"
            )
        
    @staticmethod
    def validate_init_data(init_data:str) -> dict:
        try:

            params = dict(urllib.parse.parse_qsl(init_data, keep_blank_values=True))
            hash_to_check = params.pop("hash", None)

            if not hash_to_check:
                raise HTTPException(status_code=400, detail="No hash in init_data")
            
            data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(params.items()))

            secret_key = hashlib.sha256(app_setting.BOT_TOKEN.encode()).digest()

            hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

            if not hmac.compare_digest(hmac_hash, hash_to_check):
                raise HTTPException(status_code=401, detail="Invalid init data hash")
            
            return params
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to validate init data: {e}"
            )

    @staticmethod
    async def get_user_by_id(uuid: str) -> User:
        try:
            user = await User.get(id=uuid)
            return user
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while getting user: {e}")
    
    @staticmethod
    async def get_user_by_telegram(id: int) -> User:
        try:
            user = await User.get(telegram_id=id)
            return user
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while getting user by telegram_id: {e}")
        
    