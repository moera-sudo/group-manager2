from typing import Optional, Literal
from pydantic import BaseModel, field_validator, Field

class TokenData(BaseModel):
    sub: str = Field(...)
    sub_tg: int = Field(..., ge=1)
    exp: Optional[int] = None
    iat: Optional[int] = None
    token_type: Literal["access", "refresh"]
    # came up a new method
    # @field_validator("token_type")
    # @classmethod
    # def type_validation(cls, value):
    #     if value != "refresh" and value != "access":
    #         raise ValueError('Incorrect token type')
    
    model_config = {
        'extra' : 'forbid'
    }

class Token(BaseModel):
    token: str
    token_type: Literal["access", "refresh"]


class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal['bearer'] = "bearer"
    access_token_expire: Optional[int]
    refresh_token_expire: Optional[int]


class AuthRequest(BaseModel):
    init_data: str = Field(..., description="Telegram WebApp initData (window.Telegram.WebApp.initData)")