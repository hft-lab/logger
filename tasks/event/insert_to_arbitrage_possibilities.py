import logging
from logging.config import dictConfig
from send_to_telegram import Telegram

from config import Config

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class InsertToArbitragePossibilities:
    """
    Class for insert to arbitrage_possibilities table
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'INSERT_TO_ARBITRAGE_POSSIBILITIES'
        self.telegram = Telegram(app)

    async def run(self, payload: dict) -> None:
        """
        Get cursor and start insert func
        :param payload: dict with NOT NULL values (
                    1. id,
                    2. dt,
                    3. ts,
                    4. buy_exchange,
                    5. sell_exchange,
                    6. symbol,
                    7. buy_order_id,
                    8. sell_order_id,
                    10. available_for_sell,
                    11. max_buy_vol,
                    12. max_sell_vol,
                    13. expect_buy_price,
                    14. expect_sell_price,
                    15. expect_amount_usd,
                    16. expect_amount_coin,
                    17. expect_profit_usd,
                    18. expect_profit_relative,
                    19. expect_fee_buy,
                    20. expect_fee_sell,
                    21. time_parser,
                    22. time_choose,
                    23. was_sent,
                    24. chat_id,
                    25. bot_token
                    26. shift
        :return: None
        """

        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__insert(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    async def __insert(self, data: dict, cursor) -> None:
        """
        Insert data to balancing_reports table
        :param data: dict with NOT NULL keys
        :param cursor: asyncpg cursor
        :return: None
        """
        sql = f"""
            insert into arbitrage_possibilities(
                    id,
                    datetime,
                    ts,
                    buy_exchange,
                    sell_exchange,
                    symbol,
                    buy_order_id,
                    sell_order_id,
                    max_buy_vol_usd,
                    max_sell_vol_usd,
                    expect_buy_price,
                    expect_sell_price,
                    expect_amount_usd,
                    expect_amount_coin,
                    expect_profit_usd,
                    expect_profit_relative,
                    expect_fee_buy,
                    expect_fee_sell,
                    time_parser,
                    time_choose,
                    chat_id,
                    bot_token,
                    shift,
                    status
                )
            values(
                    '{data['id']}',
                    '{data['datetime']}',
                    {data['ts']},
                    '{data['buy_exchange']}',
                    '{data['sell_exchange']}',
                    '{data['symbol']}',
                    '{data['buy_order_id']}',
                    '{data['sell_order_id']}',
                     {data['max_buy_vol_usd']},
                     {data['max_sell_vol_usd']},
                     {data['expect_buy_price']},
                     {data['expect_sell_price']},
                     {data['expect_amount_usd']},
                     {data['expect_amount_coin']},
                     {data['expect_profit_usd']},
                     {data['expect_profit_relative']},
                     {data['expect_fee_buy']},
                     {data['expect_fee_sell']},
                     {data['time_parser']},
                     {data['time_choose']},
                     '{data['chat_id']}',
                     '{data['bot_token']}',
                     {data['shift']},
                     '{data['status']}'
                )         
            """
        await cursor.execute(sql)
        await self.prepare_and_send_message_to_tg(data)

    async def prepare_and_send_message_to_tg(self, data):
        message = f"TAKER ORDER EXECUTED\n{data['sell_exch']}- | {data['buy_exch']}+\n"
        message += f"ENV: {data['env']}\n"
        message += f"DEAL STATUS: {data['status']}\n"
        message += f"PARSE TIME, SEC: {data['time_parser']}\n"
        message += f"CHOOSE DEAL TIME, SEC: {data['time_choose']}\n"
        message += f"TIME: {data['datetime']} \n"
        message += f"SELL PX: {data['sell_px']}\n"
        message += f"EXPECTED SELL PX: {data['expect_sell_px']}\n"
        message += f"BUY PX: {data['buy_px']}\n"
        message += f"EXPECTED BUY PX: {data['expect_buy_px']}\n"
        message += f"DEAL SIZE: {data['expect_amount']}\n"
        message += f"DEAL SIZE, USD: {data['expect_amount_usd']}\n"
        message += f"EXPECTED PROFIT REL, %: {data['expect_profit_relative'] * 100}\n"
        message += f"EXPECTED PROFIT ABS, USD: {data['expect_profit_usd']}\n"
        message += f"FEE SELL, %: {data['expect_fee_sell'] * 100}\n"
        message += f"FEE BUY, %: {data['expect_fee_buy'] * 100}\n"

        if data['buy_px'] == 0:
            message += f"WARNING! {data['buy_exch']} CLIENT DOESN'T CREATE ORDERS"
        elif data['sell_px'] == 0:
            message += f"WARNING! {data['sell_exch']} CLIENT DOESN'T CREATE ORDERS"

        telegram_input = {
            'chat_id': data['chat_id'],
            'bot_token': data['bot_token'],
            'msg': message
        }
        await self.telegram.run(telegram_input)




