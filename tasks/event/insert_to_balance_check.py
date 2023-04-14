import logging
from logging.config import dictConfig

from config import Config

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class InsertToBalanceCheck:
    """
    Class for insert to balance_check table
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'INSERT_TO_BALANCE_CHECK'

    async def run(self, payload: dict) -> None:
        """
        Get cursor and start insert func
        :param payload: dict with NOT NULL values (
            1. timestamp
            2. exchange_name
            3. side
            4. total_balance
            5. position
            6. available_for_buy
            7. available_for_sell
            8. env)
        :return: None
        """

        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__insert_to_balance_check(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    @staticmethod
    async def __insert_to_balance_check(data: dict, cursor) -> None:
        """
        Insert data to balancing_reports table
        :param data: dict with NOT NULL keys
        :param cursor: asyncpg cursor
        :return: None
        """
        sql = f"""
            insert into balance_check(
                ts,
                exchange_name,
                total_balance,
                pos,
                available_for_buy,
                available_for_sell,
                ask,
                bid,
                symbol,
                env,
                chat_id,
                bot_token
                )
            values(
                {data['timestamp']},
                '{data['exchange_name']}',
                {data['total_balance']},
                {data['position']},
                {data['available_for_buy']},
                {data['available_for_sell']},
                {data['ask']},
                {data['bid']},
                '{data['symbol']}',
                '{data['env']}',
                {data['chat_id']},
                '{data['bot_token']}'
                )         
            """
        await cursor.execute(sql)
