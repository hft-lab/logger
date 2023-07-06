import logging
from logging.config import dictConfig

from config import Config

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class UpdateOrders:

    def __init__(self, app):
        self.app = app
        self.worker_name = 'UPDATE_ORDERS'

    async def run(self, payload: dict) -> None:
        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__update(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    @staticmethod
    async def __update(payload, cursor) -> None:
        sql = f"""
        update 
            orders
        set 
            status = '{payload['status']}',
            factual_price = {payload['factual_price']},
            factual_amount_coin = {payload['factual_amount_coin']},
            factual_amount_usd = {payload['factual_amount_usd']},
            datetime_update = '{payload['datetime_update']}',
            ts_update = {payload['ts_update']}
        where 
            exchange = '{payload['exchange']}' and 
            exchange_order_id = '{payload['exchange_order_id']}'
        """

        await cursor.execute(sql)