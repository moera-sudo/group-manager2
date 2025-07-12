import logging
import sys
from logging.config import dictConfig
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

LOGS_DIR = BASE_DIR / "logs"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False, 

    "formatters": {
        "console_colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        
        "file_default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },

    "handlers": {
        
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console_colored",
            "level": "INFO",
            "stream": sys.stdout,
        },
        
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "file_default",
            "filename": LOGS_DIR / "bot.log", 
            "when": "D", 
            "interval": 1,
            "backupCount": 30, 
            "encoding": "utf-8",
            "level": "DEBUG", 
        },
    },

    "loggers": {
        
        "aiogram": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },

    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}


def setup_logging():
    LOGS_DIR.mkdir(exist_ok=True)
    dictConfig(LOGGING_CONFIG)
    logging.getLogger(__name__).info(f"Logging configured successfully! || LOGS_DIR:{LOGS_DIR}")