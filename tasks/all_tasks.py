from tasks.event.insert_to_arbitrage_possibilities import InsertToArbitragePossibilities
from tasks.event.insert_to_balance_detalization import InsertToBalanceDetalization
from tasks.event.insert_to_balance_jumps import InsertToBalanceJumps
from tasks.event.insert_to_balances import InsertToBalances
from tasks.event.insert_to_disbalances import InsertToDisbalance
from tasks.event.insert_to_fundings import InsertFunding
from tasks.event.insert_to_orders import InsertToOrders
from tasks.event.insert_to_ping_logger import InsertToPingLogging
from tasks.event.send_to_telegram import Telegram
from tasks.event.update_orders import UpdateOrders
from tasks.event.update_to_bot_launches import UpdateBotLaunches
from tasks.periodic.check_and_update_arbitrage_possibilities import CheckAndUpdateArbitragePossibilities
from tasks.periodic.check_and_update_disbalances import CheckAndUpdateDisbalances
from tasks.periodic.check_orders import CheckOrders

QUEUES_TASKS = {
    'logger.event.insert_ping_logger': InsertToPingLogging,
    'logger.event.send_to_telegram': Telegram,
    'logger.event.insert_balance_jumps': InsertToBalanceJumps,

    # NEW ------------------------------------------------------------------------
    'logger.event.insert_arbitrage_possibilities': InsertToArbitragePossibilities,
    'logger.event.insert_orders': InsertToOrders,
    'logger.event.insert_balances': InsertToBalances,
    'logger.event.insert_balance_detalization': InsertToBalanceDetalization,
    'logger.event.insert_disbalances': InsertToDisbalance,
    'logger.event.update_orders': UpdateOrders,
    'logger.event.insert_funding': InsertFunding,
    'logger.event.update_bot_launches': UpdateBotLaunches,

    'logger.periodic.check_and_update_arbitrage_possibilities': CheckAndUpdateArbitragePossibilities,
    'logger.periodic.check_and_update_disbalances': CheckAndUpdateDisbalances,
    'logger.periodic.check_orders': CheckOrders,
    'logger.periodic.send_to_telegram': Telegram
}

SECOND = 1
MINUTE = 60
TEN_MINUTES = MINUTE * 10
HOUR = MINUTE * 60
DAY = HOUR * 24

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
        'exchange': 'logger.periodic',
        'queue': 'logger.periodic.send_to_telegram',
        'routing_key': 'logger.periodic.send_to_telegram',
        'interval': SECOND * 10,
        'delay': SECOND,
        'payload': {
            "chat_id": -4073293077,
            "msg": "Best Hi!",
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

