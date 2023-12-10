import logging
from logging.config import dictConfig
from core.wrappers import try_exc_async


dictConfig({'version': 1, 'disable_existing_loggers': False, 'formatters': {
                'simple': {'format': '[%(asctime)s][%(threadName)s] %(funcName)s: %(message)s'}},
            'handlers': {'console': {'class': 'logging.StreamHandler', 'level': 'DEBUG', 'formatter': 'simple',
                'stream': 'ext://sys.stdout'}},
            'loggers': {'': {'handlers': ['console'], 'level': 'INFO', 'propagate': False}}})
logger = logging.getLogger(__name__)


class InsertToBalanceJumps:
    """
    Class for insert to balance_humps table
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'INSERT_TO_BALANCE_JUMPS'

    @try_exc_async
    async def run(self, payload: dict) -> None:
        """
        Get cursor and start insert func
        :param payload: dict with NOT NULL values (
            1. timestamp
            2. total_balance)
        :return: None
        """

        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__insert_to_balance_jumps(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    @staticmethod
    @try_exc_async
    async def __insert_to_balance_jumps(data: dict, cursor) -> None:
        """
        Insert data to balance_jumps table
        :param data: dict with NOT NULL keys
        :param cursor: asyncpg cursor
        :return: None
        """
        sql = f"""
            insert into balance_jumps(
                ts,
                total_balance,
                env
                )
            values(
                {data['timestamp']},
                {data['total_balance']},
                '{data['env']}'
                )         
            """
        await cursor.execute(sql)
