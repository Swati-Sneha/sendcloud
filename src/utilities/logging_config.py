import os
import logging
from logging.config import dictConfig


class CustomFilter(logging.Filter):
    def filter(self, record):
        # Exclude log records that contain specific text
        if "change detected" in record.getMessage():
            return False
        return True


def setup_logging():
    """
    Sets up logging for the entire project using a dictionary configuration.
    This can be easily extended with different handlers and formatters.
    """
        
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
            'detailed': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s (func: %(funcName)s): %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'filters': ['custom_filter']
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'logs/project.log',
                'formatter': 'detailed',
                'level': 'DEBUG',
                'filters': ['custom_filter']
            },
        },
        'filters': {
            'custom_filter': {
                '()': CustomFilter
            }, 
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
        'celery': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'uvicorn.error': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'uvicorn.access': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
    }

    dictConfig(logging_config)
