from pydantic_settings import BaseSettings
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[3] / '.env'

class BotSettings(BaseSettings):
    BOT_TOKEN: str
    API: str
    WEB_APP_URL: str

    model_config = {
        'env_file' : ENV_PATH,
        'env_file_encoding' : 'utf-8',
        'extra' : 'ignore'
    }

settings = BotSettings()