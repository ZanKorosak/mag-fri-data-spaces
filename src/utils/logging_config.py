import logging
from logging.config import dictConfig

LOG_FILE = "operations.log"

dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
        "access": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s", 
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "formatter": "default",
            "encoding": "utf8",
        },
        "access_file": {
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "formatter": "access",
            "encoding": "utf8",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
   
})