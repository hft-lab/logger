import logging
from logging.config import dictConfig

from config import Config

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class InsertToOrders:
    """
    Class for insert to orders table
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'INSERT_TO_ORDERS'

    async def run(self, payload: dict) -> None:
        """
        Get cursor and start insert func
        :param payload: dict with NOT NULL values (
                            id,
                            datetime,
                            ts,
                            context,
                            parent_id,
                            exchange_order_id,
                            type,
                            status,
                            exchange,
                            side,
                            symbol,
                            expect_price,
                            expect_amount_coin,
                            expect_amount_usd,
                            expect_fee,
                            factual_price,
                            factual_amount_coin,
                            factual_amount_usd,
                            factual_fee,
                            order_place_time,
                            env
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
            insert into orders(
                id,
                datetime,
                ts,
                context,
                parent_id,
                exchange_order_id,
                type,
                status,
                exchange,
                side,
                symbol,
                expect_price,
                expect_amount_coin,
                expect_amount_usd,
                expect_fee,
                factual_price,
                factual_amount_coin,
                factual_amount_usd,
                factual_fee,
                order_place_time,
                env
                )
            values(
                '{data['id']}',
                '{data['datetime']}',
                {data['ts']},
                '{data['context']}',
                '{data['parent_id']}',
                '{data['exchange_order_id']}',
                '{data['type']}',
                '{data['status']}',
                '{data['exchange']}',
                '{data['side']}',
                '{data['symbol']}',
                {data['expect_price']},
                {data['expect_amount_coin']},
                {data['expect_amount_usd']},
                {data['expect_fee']},
                {data['factual_price']},
                {data['factual_amount_coin']},
                {data['factual_amount_usd']},
                {data['factual_fee']},
                {data['order_place_time']},
                '{data['env']}'
                )         
            """
        await cursor.execute(sql)
