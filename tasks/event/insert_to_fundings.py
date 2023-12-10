import logging
from core.wrappers import try_exc_async


logger = logging.getLogger(__name__)


class InsertFunding:
    """
    Periodic task for check balance
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'INSERT_TO_CHECK_FUNDING'

    @try_exc_async
    async def run(self, payload: dict) -> None:
        """
        Get cursor and start insert func
        :param payload: dict with NOT NULL values (
                    1. id,
                    2. dt,
                    3. ts,
                    4. exchange_funding_id,
                    5. exchange,
                    6. symbol,
                    7. amount,
                    8. asset,
                    10. position,
                    11. price,
        :return: None
        """
        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            record = await self.__select(payload, cursor)
            if not record['count']:
                logger.info(f"INSERT: {payload}")
                await self.__insert(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    @staticmethod
    @try_exc_async
    async def __select(payload, cursor):
        sql = f"""
        SELECT
            COUNT(*)
        FROM 
            fundings 
        WHERE 
            ts = {payload['ts']} 
            AND exchange = '{payload['exchange']}'
            AND symbol = '{payload['symbol']}'
        """
        return await cursor.fetchrow(sql)

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
            insert into fundings(
                id,
                datetime,
                ts,
                exchange_funding_id,
                exchange,
                symbol,
                amount,
                asset,
                position_coin,
                price
                )
            values(
                '{data['id']}',
                '{data['datetime']}',
                {data['ts']},
                '{data['exchange_funding_id']}',
                '{data['exchange']}',
                '{data['symbol']}',
                {data['amount']},
                '{data['asset']}',
                {data['position']},
                {data['price']}
                )         
            """
        await cursor.execute(sql)
