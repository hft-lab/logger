import datetime
import logging
import time
from logging.config import dictConfig
from tasks.event.send_to_telegram import Telegram

dictConfig({'version': 1, 'disable_existing_loggers': False, 'formatters': {
                'simple': {'format': '[%(asctime)s][%(threadName)s] %(funcName)s: %(message)s'}},
            'handlers': {'console': {'class': 'logging.StreamHandler', 'level': 'DEBUG', 'formatter': 'simple',
                'stream': 'ext://sys.stdout'}},
            'loggers': {'': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False}}})
logger = logging.getLogger(__name__)


class OrderStatuses:
    SUCCESS = 'Fully Executed'
    UNSUCCESS = 'Not Executed'


class ArbitragePossibilitiesStatuses:
    SUCCESS = 'Success'
    UNSUCCESS = 'Unsuccess'
    DISBALANCE = 'Disbalance'


class CheckAndUpdateArbitragePossibilities:
    ROUTING_KEY = 'logger.event.check_balance'
    EXCHANGE_NAME = 'logger.event.'
    QUEUE_NAME = 'logger.event.check_balance'

    def __init__(self, app):
        self.app = app
        self.worker_name = 'CHECK_AND_UPDATE_ARBITRAGE_POSSIBILITIES'
        self.all_arbitrage_possibilities = []
        self.arbitrage_possibilities_to_update = []
        self.telegram = Telegram(app)

    async def run(self, payload: dict) -> None:
        logger.info(f"Start: {self.worker_name}")

        async with self.app['db'].acquire() as cursor:
            await self.__get_all_processing_arbitrage_possibilities_ids(cursor)
            await self.__get_orders_by_parent_id(cursor)
            await self.__update_arbitrage_possibilities(cursor)

        logger.info(f"Finish: {self.worker_name}")

    async def __get_all_processing_arbitrage_possibilities_ids(self, cursor):
        sql = """
        select 
            *
        from 
           arbitrage_possibilities
        where 
            status = 'Processing'
        order by
            ts desc
        """

        self.all_arbitrage_possibilities = await cursor.fetch(sql)

    async def __get_orders_by_parent_id(self, cursor):
        for possibility in self.all_arbitrage_possibilities:
            parent_id = possibility["id"]
            sql = f"""
            select 
                *
            from
                orders
            where 
                parent_id = '{parent_id}'
            """
            data = await cursor.fetch(sql)
            in_processing = False
            else_statuses = []

            for row in data:
                if row['status'] == 'Processing':
                    in_processing = True
                elif row['status'] == OrderStatuses.SUCCESS:
                    else_statuses.append(True)
                elif row['status'] == OrderStatuses.UNSUCCESS:
                    else_statuses.append(False)

            if not in_processing and all(else_statuses):
                self.arbitrage_possibilities_to_update.append(
                    {
                        'id': parent_id,
                        'status': ArbitragePossibilitiesStatuses.SUCCESS,
                        'status_datetime': datetime.datetime.utcnow(),
                        'status_ts': time.time(),
                        'possibility': possibility,
                        'orders': data
                    }
                )
            elif not in_processing and any(else_statuses):
                self.arbitrage_possibilities_to_update.append(
                    {
                        'id': parent_id,
                        'status': ArbitragePossibilitiesStatuses.DISBALANCE,
                        'status_datetime': datetime.datetime.utcnow(),
                        'status_ts': time.time(),
                        'possibility': possibility,
                        'orders': data
                    }
                )
            elif not in_processing and not all(else_statuses):
                self.arbitrage_possibilities_to_update.append(
                    {
                        'id': parent_id,
                        'status': ArbitragePossibilitiesStatuses.UNSUCCESS,
                        'status_datetime': datetime.datetime.utcnow(),
                        'status_ts': time.time(),
                        'possibility': possibility,
                        'orders': data

                    }
                )

    async def __update_arbitrage_possibilities(self, cursor):
        for data in self.arbitrage_possibilities_to_update:
            sql = f"""
                    update 
                        arbitrage_possibilities
                    set 
                        status = '{data['status']}',
                        status_datetime = '{data['status_datetime']}',
                        status_ts = {data['status_ts']}
                    where 
                        id = '{data['id']}'
                    """

            await cursor.execute(sql)
            await self.prepare_and_send_message_to_tg(data['orders'], data['possibility'])

    async def prepare_and_send_message_to_tg(self, data, possibility):
        if len(data) == 2:
            sell_order = [x for x in data if x['side'] == 'sell'][0]
            buy_order = [x for x in data if x['side'] == 'buy'][0]
            status = 'Unsuccessful'

            if sell_order['status'] == OrderStatuses.SUCCESS and buy_order['status'] == OrderStatuses.SUCCESS:
                status = 'Success'

            factual_size_coin = min([sell_order['factual_amount_coin'], buy_order['factual_amount_coin']])
            factual_size_usd = min([sell_order['factual_amount_usd'], buy_order['factual_amount_usd']])
            disbalance_coin = buy_order['expect_amount_coin'] - factual_size_coin
            disbalance_usd = buy_order['expect_amount_usd'] - factual_size_usd

            try:
                profit = (sell_order['factual_price'] - buy_order['factual_price']) / buy_order['factual_price']
            except ZeroDivisionError:
                profit = 0

            profit_with_fees = profit - sell_order['factual_fee'] - buy_order['factual_fee']

            message = f"TAKER ORDER EXECUTED\n"
            message += f"{sell_order['exchange']}- | {buy_order['exchange']}+\n"
            message += f"ENV: {sell_order['env']}\n"
            message += f"DEAL STATUS: {status}\n"
            message += f"DEAL TIME: {str(buy_order['datetime']).split('.')[0]}\n"
            message += f"FACTUAL SELL PX: {sell_order['factual_price']}\n"
            message += f"EXPECT SELL PX: {possibility['expect_sell_price']}\n"
            message += f"LIMIT SELL PX: {sell_order['expect_price']}\n"
            message += f"FACTUAL BUY PX: {buy_order['factual_price']}\n"
            message += f"EXPECT BUY PX: {possibility['expect_buy_price']}\n"
            message += f"LIMIT BUY PX: {buy_order['expect_price']}\n"
            message += f"DEAL SIZE: {round(factual_size_coin, 3)}\n"
            message += f"DEAL SIZE, USD: {round(factual_size_usd, 3)}\n"
            message += f"DISBALANCE: {round(disbalance_coin, 3)}\n"
            message += f"DISBALANCE, USD: {round(disbalance_usd, 3)}\n"
            message += f"PROFIT REL, %: {round(profit_with_fees * 100, 3)}\n"
            message += f"PROFIT ABS, USD: {round(profit_with_fees * factual_size_usd, 3)}\n"
            message += f"FEE SELL, %: {round(sell_order['factual_fee'] * 100, 3)}\n"
            message += f"FEE BUY, %: {round(buy_order['factual_fee'] * 100, 3)}\n"

        else:
            message = f"***** AP {possibility['id']} has less than two orders in DB *****"

        telegram_input = {
            'chat_id': possibility['chat_id'],
            'bot_token': possibility['bot_token'],
            'msg': message
        }
        await self.telegram.run(telegram_input)
