from pydantic_settings import BaseSettings
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[4] / '.env'

class AuthSettings(BaseSettings):
    
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE: int
    REFRESH_TOKEN_EXPIRE: int

    model_config = {
        'env_file' : ENV_PATH,
        'env_file_encoding' : 'utf-8',
        'extra' : 'ignore'
    }

settings = AuthSettings()