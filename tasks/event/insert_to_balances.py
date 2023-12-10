import logging
from logging.config import dictConfig
from core.wrappers import try_exc_async


dictConfig({'version': 1, 'disable_existing_loggers': False, 'formatters': {
                'simple': {'format': '[%(asctime)s][%(threadName)s] %(funcName)s: %(message)s'}},
            'handlers': {'console': {'class': 'logging.StreamHandler', 'level': 'DEBUG', 'formatter': 'simple',
                'stream': 'ext://sys.stdout'}},
            'loggers': {'': {'handlers': ['console'], 'level': 'INFO', 'propagate': False}}})
logger = logging.getLogger(__name__)


class InsertToBalances:
    """
    Class for insert to balances table
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'INSERT_TO_BALANCES'

    @try_exc_async
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
                exchange_balance,
                exchange_available_for_buy,
                exchange_available_for_sell,
                was_sent,
                chat_id,
                bot_token
        :return: None
        """

        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__insert(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    @staticmethod
    @try_exc_async
    async def __insert(data: dict, cursor) -> None:
        """
        Insert data to balancing_reports table
        :param data: dict with NOT NULL keys
        :param cursor: asyncpg cursor
        :return: None
        """
        sql = f"""
            insert into balances(
                id,
                datetime,
                ts,
                context,
                parent_id,
                exchange,
                exchange_balance,
                available_for_buy,
                available_for_sell,
                env,
                chat_id,
                bot_token,
                current_margin               
                )
            values(
                '{data['id']}',
                '{data['datetime']}',
                {data['ts']},
                '{data['context']}',
                '{data['parent_id']}',
                '{data['exchange']}',
                {data['exchange_balance']},
                {data['available_for_buy']},
                {data['available_for_sell']},
                '{data['env']}',
                {data['chat_id']},
                '{data['bot_token']}',
                {data['current_margin']}
                )         
            """
        await cursor.execute(sql)
