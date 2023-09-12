import logging
from logging.config import dictConfig

dictConfig({'version': 1, 'disable_existing_loggers': False, 'formatters': {
                'simple': {'format': '[%(asctime)s][%(threadName)s] %(funcName)s: %(message)s'}},
            'handlers': {'console': {'class': 'logging.StreamHandler', 'level': 'DEBUG', 'formatter': 'simple',
                'stream': 'ext://sys.stdout'}},
            'loggers': {'': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False}}})
logger = logging.getLogger(__name__)


class InsertToDisbalance:
    """
    Class for insert to disbalances table
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'INSERT_TO_DISBALANCES'

    async def run(self, payload: dict) -> None:
        """
        Get cursor and start insert func
        :param payload: dict with NOT NULL values (
                id,
                datetime,
                ts,
                coin_name,
                position_coin,
                position_usd,
                price
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
            insert into disbalances(
                id,
                datetime,
                ts,
                coin_name,
                position_coin,
                position_usd,
                price,
                threshold,
                status
                )
            values(
                '{data['id']}',
                '{data['datetime']}',
                {data['ts']},
                '{data['coin_name']}',
                {data['position_coin']},
                {data['position_usd']},
                {data['price']},
                {data['threshold']},
                '{data['status']}'
                )         
            """
        await cursor.execute(sql)
