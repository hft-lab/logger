import logging
from logging.config import dictConfig

from config import Config

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class InsertToBalanceDetalization:
    """
    Class for insert to balance_detalization table
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'INSERT_TO_BALANCE_DETALIZATION'

    async def run(self, payload: dict) -> None:
        """
        Get cursor and start insert func
        :param payload: dict with NOT NULL values (
                        id,
                        dt,
                        ts,
                        context,
                        parent_id,
                        exchange,
                        side,
                        symbol,
                        max_margin,
                        current_margin,
                        position_coin,
                        position_usd,
                        entry_price,
                        mark_price
        :return: None
        """

        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__insert(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    @staticmethod
    async def __insert(data: dict, cursor) -> None:
        """
        Insert data to balancing_reports table
        :param data: dict with NOT NULL keys
        :param cursor: asyncpg cursor
        :return: None
        """
        sql = f"""
            insert into balance_detalization(
                        id,
                        datetime,
                        ts,
                        context,
                        parent_id,
                        exchange,
                        side,
                        symbol,
                        max_margin,
                        current_margin,
                        position_coin,
                        position_usd,
                        entry_price,
                        mark_price
                )
            values(
                        '{data['id']}',
                        '{data['datetime']}',
                        {data['ts']},
                        '{data['context']}',
                        '{data['parent_id']}',
                        '{data['exchange']}',
                        '{data['side']}',
                        '{data['symbol']}',
                        {data['max_margin']},
                        {data['current_margin']},
                        {data['position_coin']},
                        {data['position_usd']},
                        {data['entry_price']}',
                        {data['mark_price']}
                )         
            """
        await cursor.execute(sql)
