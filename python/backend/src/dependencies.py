# Here you need to write all the dependencies that will be used throughout the application, the most important: get_current_user.
# If there are a lot of them, I will split them into different files

from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from .auth.models import User
from .auth.service import Service as AuthService

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="da_hui_znaet_ezhe")

async def get_current_user(token: Annotated[str, Depends(oauth_2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_data = AuthService.decode_jwt(token, "access")

        if token_data is None:
            raise credentials_exception
        
        user = await AuthService.get_user_by_id(uuid=token_data.sub)

        if user is None:
            raise credentials_exception
        
        return user
    
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Failed to get user: {e}"
        )