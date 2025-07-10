import logging
from logging.config import dictConfig
import os
from pathlib import Path

from .settings import settings
from ..models import MODELS

# Tortoise orm connection 
TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    },
    "apps" : {
        "models": {
            "models": MODELS,
            "default_connection": "default",
        }
        
    }
}


# Settings for logs
BASE_DIR = Path(__file__).resolve().parents[2]

LOGS_DIR = BASE_DIR / "logs"

LOGGING_CONFIG_DEBUG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "console_colored": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": "%(levelprefix)s %(asctime)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console_colored",
            "level": "INFO",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "default",
            "filename": LOGS_DIR / "app.log",
            "when": "D",
            "interval": 1,
            "backupCount": 30,
            "encoding": "utf-8",
            "level": "INFO",
        },
    },
    "loggers": {
        # root logger
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True
        },
        # access logger for uvicorn.access
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        # Logger for uvicorn errors
        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False
        },
    },
}

# To disable logs in prod
LOGGING_CONFIG_PROD = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },

    "loggers": {
        "": {"handlers": ["null"], "level": "INFO", "propagate": True},
        "uvicorn.access": {"handlers": ["null"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"handlers": ["null"], "level": "WARNING", "propagate": False},
    }
}


def setup_logging(debug: bool = False):

    if debug:
        os.makedirs(LOGS_DIR, exist_ok=True)
        dictConfig(LOGGING_CONFIG_DEBUG)
        logging.getLogger("src.core.config").info("Logging configured for DEBUG mode.")
    else:
        dictConfig(LOGGING_CONFIG_PROD)