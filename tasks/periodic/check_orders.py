import logging
from logging.config import dictConfig

from core.rabbit_mq import publish_message
from core.wrappers import try_exc_async


dictConfig({'version': 1, 'disable_existing_loggers': False, 'formatters': {
                'simple': {'format': '[%(asctime)s][%(threadName)s] %(funcName)s: %(message)s'}},
            'handlers': {'console': {'class': 'logging.StreamHandler', 'level': 'DEBUG', 'formatter': 'simple',
                'stream': 'ext://sys.stdout'}},
            'loggers': {'': {'handlers': ['console'], 'level': 'INFO', 'propagate': False}}})
logger = logging.getLogger(__name__)


class CheckOrders:
    ROUTING_KEY = 'logger.event.get_orders_results'
    EXCHANGE_NAME = 'logger.event'
    QUEUE_NAME = 'logger.event.get_orders_results'

    def __init__(self, app):
        self.app = app
        self.worker_name = 'CHECK_ORDERS'

    @try_exc_async
    async def run(self, payload: dict) -> None:
        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__get_and_send_orders_by_exchange_name(cursor)
        logger.info(f"Finish: {self.worker_name}")

    @try_exc_async
    async def __get_and_send_orders_by_exchange_name(self, cursor):
        sql = f"""
        select 
            o.exchange_order_id as orders_ids,
            o.exchange,
            o.symbol 
        from 
            orders o 
        where 
            o.exchange_order_id != 'default' and 
            o.status = 'Processing' and 
            (CURRENT_TIMESTAMP - INTERVAL '4 minutes') AT TIME ZONE 'UTC' > o.datetime
        order by 
            ts desc
        limit 
            3
        """

        if data := await cursor.fetch(sql):
            messages = []
            for order in data:
                messages.append({
                        'symbol': order['symbol'],
                        'order_ids': order['orders_ids'],
                        'exchange': order['exchange']
                    })

            await publish_message(
                    connection=self.app['mq'],
                    message=messages,
                    exchange_name=self.EXCHANGE_NAME,
                    routing_key=self.ROUTING_KEY,
                    queue_name=self.QUEUE_NAME
                )
