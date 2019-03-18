import logging
import logging.config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


__all__ = ['Session']


LOGGING_CONFIGURATION = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        'opg_scraper': {
            'level': 'INFO',
            'propagate': True,
            'handlers': ['console'],
        }
    }
}


logging.config.dictConfig(LOGGING_CONFIGURATION)


_engine = create_engine('sqlite:///opg.db', echo=True)


Session = sessionmaker(bind=_engine)
