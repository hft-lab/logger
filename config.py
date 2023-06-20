import os

from dotenv import load_dotenv

load_dotenv()

SECOND = 1
MINUTE = 60
TEN_MINUTES = MINUTE * 10
HOUR = MINUTE * 60
DAY = HOUR * 24

class Config:
    """
    Config class
    """

    POSTGRES = {
        'database': os.getenv('POSTGRES_NAME'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
    }

    RABBIT = {
        'host': os.getenv('RABBIT_MQ_HOST'),
        'port': int(os.getenv('RABBIT_MQ_PORT')),
        'username': os.getenv('RABBIT_MQ_USER'),
        'password': os.getenv('RABBIT_MQ_PASSWORD')
    }

    PERIODIC_TASKS = [
        {
            'exchange': 'logger.periodic',
            'queue': 'logger.periodic.check_orders',
            'routing_key': 'logger.periodic.check_orders',
            'interval': SECOND * 30,
            'delay': SECOND * 10,
            'payload': {}
        },
        {
            'exchange': 'logger.periodic',
            'queue': 'logger.periodic.check_and_update_arbitrage_possibilities',
            'routing_key': 'logger.periodic.check_and_update_arbitrage_possibilities',
            'interval': SECOND * 5,
            'delay': SECOND * 5,
            'payload': {}
        },
        {
            'exchange': 'logger.periodic',
            'queue': 'logger.periodic.check_and_update_disbalances',
            'routing_key': 'logger.periodic.check_and_update_disbalances',
            'interval': SECOND * 5,
            'delay': SECOND * 5,
            'payload': {}
        }
    ]

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '[%(asctime)s][%(threadName)s] %(funcName)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False
            },
        }
    }
