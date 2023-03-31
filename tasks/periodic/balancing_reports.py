import asyncio

from config import Config
from core.base_periodic_task import BasePeriodicTask


class BalancingReports(BasePeriodicTask):
    """
    Periodic task for balancing reports
    """

    ROUTING_KEY = 'logger.event.send_message'
    EXCHANGE_NAME = 'logger.event'
    QUEUE_NAME = 'logger.event.send_message'
    CHAT_ID = Config.TELEGRAM_CHAT_ID

    async def prepare_message(self):
        if self.data:
            coin = self.data['coin'].split('USD')[0].replace('-', '').replace('/', '')
            size_usd = abs(round(self.data['position_gap'] * self.data['price'], 2))
            message = f"CREATED BALANCING ORDER\n"
            message += f"SIZE, {coin}: {self.data['position_gap']}\n"
            message += f"SIZE, USD: {size_usd}\n"
            message += f"PRICE: {round(self.data['price'], 2)}\n"
            message += f"SIDE: {self.data['side']}\n"
            message += f"TAKER FEE: {self.data['taker_fee']}\n"
            message += f"TIMESTAMP, SEC: {round(self.data['ts'])}"

            await self.__update_one(self.data['ts'], self.data['exchange_name'])

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
            balancing_reports
        where
            was_sent = False
        order by
            ts
        limit 
            1
        """
        self.data = await self.cursor.fetchrow(sql)

    async def __update_one(self, ts, exchange_name):
        sql = f"""
                  update 
                      balancing_reports
                  set 
                      was_sent = True
                  where
                       was_sent = False and 
                       ts = {ts} and 
                       exchange_name = '{exchange_name}'
                  """

        await self.cursor.execute(sql)


if __name__ == '__main__':
    worker = BalancingReports()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(worker.run())
    except Exception as e:
        print(e)
    finally:
        loop.close()
