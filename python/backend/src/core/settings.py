from pydantic_settings import BaseSettings
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[4] / '.env'


class AppSettings(BaseSettings):
    # App Settings for fastapi
    APP_NAME: str
    APP_VERSION: str 
    APP_DESC: str
    DEBUG: bool

    # Settings for database
    DB_USERNAME: str = 'postgres'
    DB_NAME: str
    DB_PASSWORD: str = '123'
    DB_HOST: str = 'localhost'
    DB_PORT: str = '5432'
    DB_DRIVER: str = 'asyncpg'

    # BOT Token
    BOT_TOKEN: str

    model_config = {
        'env_file' : ENV_PATH,
        'env_file_encoding' : 'utf-8',
        'extra' : 'ignore'
        }
    

settings = AppSettings()