import logging
from logging.config import dictConfig

from config import Config

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class InsertToDealsReports:
    """
    Class for insert to deals_report table
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'INSERT_TO_DEALS_REPORTS'

    async def run(self, payload: dict) -> None:
        """
        Get cursor and start insert func
        :param payload: dict with NOT NULL values (
            1. timestamp
            2. sell exchange
            3. buy_exchange
            4. sell_px
            5. expect_sell_px
            6. buy_px
            7. expect_buy_px
            8. amount_USD
            9. amount_coin
            10. profit_USD
            11. profit_relative
            12. fee_sell
            13. fee_buy
            14. long_side
            15. sell_ob_ask
            16. buy_ob_bid
            17. deal_time
            18. time_parser
            19. time_choose
            20. env)
        :return: None
        """

        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__insert_to_report_message(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    @staticmethod
    async def __insert_to_report_message(data: dict, cursor) -> None:
        """
        Insert data to deals_reports table
        :param data: dict with NOT NULL keys
        :param cursor: asyncpg cursor
        :return: None
        """
        sql = f"""
            insert into deals_reports(
                ts,
                date_utc,
                sell_order_id,
                buy_order_id,
                sell_exch,
                buy_exch,
                sell_px, 
                expect_sell_px,
                buy_px,
                expect_buy_px,
                amount_USD,
                amount_coin,
                profit_USD,
                profit_relative,
                fee_sell,
                fee_buy,
                long_side,
                sell_ob_ask,
                buy_ob_bid,
                deal_time,
                time_parser,
                time_choose,
                env,
                coin,
                chat_id,
                bot_token
                )
            values(
                {data['timestamp']},
                '{data['date_utc']}',
                '{data['sell_order_id']}',
                '{data['buy_order_id']}',
                '{data['sell_exch']}',
                '{data['buy_exch']}',
                {data['sell_px']},
                {data['expect_sell_px']},
                {data['buy_px']},
                {data['expect_buy_px']},
                {data['amount_USD']},
                {data['amount_coin']},
                {data['profit_USD']},
                {data['profit_relative']},
                {data['fee_sell']},
                {data['fee_buy']},
                '{data['long_side']}',
                {data['sell_ob_ask']},
                {data['buy_ob_bid']},
                {data['deal_time']},
                {data['time_parser']},
                {data['time_choose']},
                '{data['env']}',
                '{data['coin']}',
                {data['chat_id']},
                '{data['bot_token']}'
                )         
            """
        await cursor.execute(sql)
