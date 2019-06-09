"""
Created on 16.03.2019

@author: wagnerpeer

Define basic logging format and the sqlalchemy session to be used throughout
the package.
"""
__all__ = []

import logging
import logging.config

from . import controler
from .controler import *
from . import storage
from .storage import *

__all__ += controler.__all__
__all__ += storage.__all__


LOGGING_CONFIGURATION = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "opg_scraper": {"level": "INFO", "propagate": True, "handlers": ["console"]}
    },
}

logging.config.dictConfig(LOGGING_CONFIGURATION)
