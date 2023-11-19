import configparser
import sys
config = configparser.ConfigParser()
config.read(sys.argv[1], "utf-8")


SECOND = 1
MINUTE = 60
TEN_MINUTES = MINUTE * 10
HOUR = MINUTE * 60
DAY = HOUR * 24

class Config:
    """
    Config class
    """
    setts = config['POSTGRES']
    POSTGRES = {
        'database': setts['NAME'],
        'user': setts['USER'],
        'password': setts['PASSWORD'],
        'host': setts['HOST'],
        'port': setts['PORT'],
    }

    setts = config['RABBIT']
    RABBIT = {
        'host': setts['HOST'],
        'port': int(setts['PORT']),
        'username': setts['USERNAME'],
        'password': setts['PASSWORD']
    }

    RABBIT_URL = f"amqp://{RABBIT['username']}:{RABBIT['password']}@{RABBIT['host']}:{RABBIT['port']}/"

    PERIODIC_TASKS = [
        {
            'exchange': 'logger.periodic',
            'queue': 'logger.periodic.check_orders',
            'routing_key': 'logger.periodic.check_orders',
            'interval': MINUTE,
            'delay': SECOND * 30,
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
        },
        {
            'exchange': 'logger.event',
            'queue': 'logger.event.send_to_telegram',
            'routing_key': 'logger.event.send_to_telegram',
            'interval': SECOND * 10,
            'delay': SECOND,
            'payload': {
                "chat_id": -4073293077,
                "msg": "Hi from Dima",
                'bot_token': '6684267405:AAFf2z4yVXtW-afd3kM7vAfNkNipCJBAZbw'
            }
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
