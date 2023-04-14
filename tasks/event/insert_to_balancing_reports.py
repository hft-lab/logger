import logging
from logging.config import dictConfig

from config import Config

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class InsertToBalancingReports:
    """
    Class for insert to balancing_report table
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'INSERT_TO_BALANCING_REPORTS'

    async def run(self, payload: dict) -> None:
        """
        Get cursor and start insert func
        :param payload: dict with NOT NULL values (
            1. timestamp
            2. exchange_name
            3. side
            4. price
            5. taker_fee
            6. position_gap
            7. size_usd
            8. coin
            9. env)
        :return: None
        """

        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__insert_to_balancing_reports(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    @staticmethod
    async def __insert_to_balancing_reports(data: dict, cursor) -> None:
        """
        Insert data to balancing_reports table
        :param data: dict with NOT NULL keys
        :param cursor: asyncpg cursor
        :return: None
        """
        sql = f"""
            insert into balancing_reports(
                ts,
                exchange_name,
                side,
                price,
                taker_fee,
                position_gap,
                size_usd,
                env,
                coin,
                chat_id,
                bot_token
                )
            values(
                {data['timestamp']},
                '{data['exchange_name']}',
                '{data['side']}',
                {data['price']},
                {data['taker_fee']},
                {data['position_gap']},
                {data['size_usd']},
                '{data['env']}',
                '{data['coin']}',
                {data['chat_id']},
                '{data['bot_token']}'
                )         
            """
        await cursor.execute(sql)
