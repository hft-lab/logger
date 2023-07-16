import logging
from logging.config import dictConfig

from config import Config

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class InsertToBotLaunches:
    """
    Class for insert to bot_launches table
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'INSERT_TO_BOT_LAUNCHES'

    async def run(self, payload: dict) -> None:
        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__insert(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    async def __insert(self, data: dict, cursor) -> None:
        """
        Insert data to bot_launches table
        :param data: dict with NOT NULL keys
        :param cursor: asyncpg cursor
        :return: None
        """
        sql = f"""
            insert into bot_launches(
                    id,
                    datetime,
                    ts,
                    exchange_1,
                    exchange_2,
                    coin,
                    env,
                    fee_exchange_1,
                    fee_exchange_2,
                    shift,
                    order_delay,
                    max_order_usd,
                    max_leverage,
                    target_profit
                )
            values(
                    '{data['id']}',
                    '{data['datetime']}',
                    {data['ts']},
                    '{data['exchange_1']}',
                    '{data['exchange_2']}',
                    '{data['coin']}',
                    '{data['env']}',
                     {data['fee_exchange_1']},
                     {data['fee_exchange_2']},
                     {data['shift']},
                     {data['order_delay']},
                     {data['max_order_usd']},
                     {data['max_leverage']},
                     {data['profit_taker']}
                )         
            """
        await cursor.execute(sql)




