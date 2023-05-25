import logging
from logging.config import dictConfig

from config import Config
from core.rabbit_mq import publish_message

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)

class CheckOrders:
    ROUTING_KEY = 'logger.event.get_orders_results'
    EXCHANGE_NAME = 'logger.event'
    QUEUE_NAME = 'logger.event.get_orders_results'

    def __init__(self, app):
        self.app = app
        self.worker_name = 'CHECK_ORDERS'

    async def run(self, payload: dict) -> None:
        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__get_orders_in_processing(cursor)

            for exchange in self.exchanges_names:
                await self.__get_and_send_orders_by_exchange_name(exchange, cursor)

        logger.info(f"Finish: {self.worker_name}")


    async def __get_orders_in_processing(self, cursor) -> None:
        sql = """
        select 
            distinct on (exchange) exchange as exchanges
        from 
            orders
        """

        self.exchanges_names = [x['exchanges'] for x in await cursor.fetch(sql)]

    async def __get_and_send_orders_by_exchange_name(self, exchange, cursor):
        sql = f"""
        select 
            o.exchange_order_id as orders_ids
        from 
            orders o 
        where 
            o.exchange = '{exchange}' and 
            o.exchange_order_id != 'default'
        order by 
            ts desc
        limit 
            5
        """

        if data := await cursor.fetch(sql):
            await publish_message(
                connection=self.app['mq'],
                message= [x['orders_ids'] for x in data] + [exchange],
                exchange_name=self.EXCHANGE_NAME,
                routing_key=self.ROUTING_KEY,
                queue_name=self.QUEUE_NAME,
            )



