import asyncio
import traceback
from datetime import datetime

from config import Config
from core.base_periodic_task import BasePeriodicTask


class DealsReports(BasePeriodicTask):
    """
    Periodic task for deals reports
    """
    ROUTING_KEY = 'logger.event.send_message'
    EXCHANGE_NAME = 'logger.event'
    QUEUE_NAME = 'logger.event.send_message'
    CHAT_ID = Config.TELEGRAM_CHAT_ID

    async def prepare_message(self):
        if self.data:
            message = f"TAKER ORDER EXECUTED\n{self.data['sell_exch']}- | {self.data['buy_exch']}+\n"
            message += f"CREATE ORDERS TIME, SEC: {round(self.data['deal_time'], 6)}\n"
            message += f"PARSE TIME, SEC: {round(self.data['time_parser'], 6)}\n"
            message += f"CHOOSE DEAL TIME, SEC: {round(self.data['time_choose'], 6)}\n"
            message += f"TIME: {datetime.fromtimestamp(int(float(round(self.data['ts'] / 1000))))} \n"
            message += f"SELL PX: {round(self.data['sell_px'], 2)}\n"
            message += f"EXPECTED SELL PX: {round(self.data['expect_sell_px'], 2)}\n"
            message += f"SELL EXCHANGE TOP ASK: {self.data['sell_ob_ask']}\n"
            message += f"BUY PX: {self.data['buy_px']}\n"
            message += f"EXPECTED BUY PX: {self.data['expect_buy_px']}\n"
            message += f"BUY EXCHANGE TOP BID: {self.data['buy_ob_bid']}\n"
            message += f"DEAL SIZE: {round(self.data['amount_coin'], 6)}\n"
            message += f"DEAL SIZE, USD: {round(self.data['amount_usd'])}\n"
            message += f"PROFIT REL, %: {round(self.data['profit_relative'] * 100, 4)}\n"
            message += f"PROFIT ABS, USD: {round(self.data['profit_usd'], 2)}\n"
            message += f"FEE SELL, %: {round(self.data['fee_sell'] * 100, 6)}\n"
            message += f"FEE BUY, %: {round(self.data['fee_buy'] * 100, 6)}\n"
            if self.data['buy_px'] == 0:
                message += f"WARNING! {self.data['buy_exch']} CLIENT DOESN'T CREATE ORDERS"
            elif self.data['sell_px'] == 0:
                message += f"WARNING! {self.data['sell_exch']} CLIENT DOESN'T CREATE ORDERS"

            await self.__update_one(self.data['ts'], self.data['sell_exch'], self.data['buy_exch'])

            self.data = {
                'chat_id': self.CHAT_ID,
                'msg': message
            }
            await self.send_to_rabbit()

    async def get_data(self):
            sql = """
            select 
                *
            from  
                deals_reports as dr
            where
                dr.was_sent = False
            order by
                dr.ts asc
            limit 
                1
            """
            self.data = await self.cursor.fetchrow(sql)

    async def __update_one(self, ts, sell_exch, buy_exch):
            sql = f"""
               update 
                   deals_reports
               set 
                   was_sent = True
               where
                    was_sent = False and 
                    ts = {ts} and 
                    sell_exch = '{sell_exch}' and 
                    buy_exch = '{buy_exch}'
               """

            await self.cursor.execute(sql)


if __name__ == '__main__':
    worker = DealsReports()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(worker.run())
    except Exception as e:
        traceback.print_exc()
    finally:
        loop.close()
